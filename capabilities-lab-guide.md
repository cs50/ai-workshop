# Linux Process Capabilities Lab Guide

## Student Hands-On Lab: Secure Web Server with Process Capabilities

---

## Lab Overview

This hands-on lab demonstrates how Linux capabilities provide fine-grained privilege control, allowing processes to perform specific privileged operations without running as root. You'll create a secure web server that binds to port 80 (a privileged port) while running as a non-root user.

**Duration:** 30-45 minutes

**Difficulty:** Intermediate

---

## Learning Objectives

By the end of this lab, you will be able to:

1. Understand the concept of Linux capabilities and their role in the principle of least privilege
2. Use capability tools (`getcap`, `setcap`) to view and modify file capabilities
3. Configure a process to bind to privileged ports (< 1024) without root access
4. Analyze process capabilities using `/proc` filesystem
5. Verify security boundaries and limitations of capability-enabled processes
6. Distinguish between different capability sets (Permitted, Effective, Inheritable, etc.)

---

## Theory Overview

### What are Linux Capabilities?

Traditional UNIX systems divide processes into two categories:
- **Privileged processes (UID 0/root)**: Can bypass all kernel permission checks
- **Unprivileged processes (non-zero UID)**: Subject to full permission checking

This binary model is inflexible and violates the **principle of least privilege**. Linux capabilities divide root privileges into distinct units called **capabilities**, which can be independently enabled or disabled.

### Why Use Capabilities?

**Problem:** Many services need only one or two root privileges but traditionally run as full root, creating unnecessary security risks.

**Solution:** Capabilities allow you to grant specific privileges to processes without giving full root access.

**Example:** A web server needs to bind to port 80 (privileged) but doesn't need to:
- Read any file on the system
- Kill other processes
- Load kernel modules
- Change system time

### Key Capability Sets

Each process has several capability sets:

- **Permitted (CapPrm)**: Capabilities the process may use
- **Effective (CapEff)**: Capabilities currently active
- **Inheritable (CapInh)**: Capabilities preserved across `execve()`
- **Bounding (CapBnd)**: Limiting superset of capabilities
- **Ambient (CapAmb)**: Capabilities preserved for non-root processes

### Common Capabilities

| Capability | Description |
|------------|-------------|
| `CAP_NET_BIND_SERVICE` | Bind to ports < 1024 |
| `CAP_NET_ADMIN` | Network administration operations |
| `CAP_SYS_TIME` | Set system clock |
| `CAP_CHOWN` | Change file ownership |
| `CAP_KILL` | Send signals to other processes |
| `CAP_SYS_ADMIN` | General system administration |

### The `CAP_NET_BIND_SERVICE` Capability

In this lab, we focus on `CAP_NET_BIND_SERVICE`, which allows binding to privileged ports (ports 0-1023) without being root. This is perfect for web servers that need port 80 or 443.

---

## Lab Environment

### Docker Setup

This lab runs in a Docker container with the necessary tools pre-installed.

**Container specifications:**
- Base image: Ubuntu/Debian with Python 3
- Required packages: `libcap2-bin`, `python3`, `curl`
- User: Regular non-root user (UID 1000)
- Capabilities support: Enabled

**Starting the lab environment:**

```bash
# Pull and run the lab container
docker run -it --rm \
  --cap-add=ALL \
  --name capabilities-lab \
  ubuntu:22.04 /bin/bash

# Inside container, install required tools
apt-get update && apt-get install -y \
  libcap2-bin \
  python3 \
  curl \
  sudo \
  procps

# Create a regular user
useradd -m -s /bin/bash student
echo "student ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
su - student
```

---

## Lab Exercises

### Exercise 1: Understanding the Problem (5 minutes)

**Objective:** Demonstrate that normal users cannot bind to privileged ports.

#### Step 1: Create a Simple Web Server

```bash
# Create a minimal web server
cat > secure_server.py << 'EOF'
#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys

PORT = 80

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stderr.write(f"[UID {os.getuid()}] {format % args}\n")

print(f"Starting server on port {PORT} as UID {os.getuid()}")
print(f"Effective UID: {os.geteuid()}")
print(f"Process PID: {os.getpid()}")

# Check capabilities
print("\nChecking capabilities...")
try:
    with open(f'/proc/{os.getpid()}/status') as f:
        for line in f:
            if 'Cap' in line:
                print(f"  {line.strip()}")
except Exception as e:
    print(f"  Could not read capabilities: {e}")

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"\nServer running. Test with: curl http://localhost:{PORT}")
    print("Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
EOF

chmod +x secure_server.py
```

#### Step 2: Try Running as Normal User

```bash
./secure_server.py
```

**Expected Result:**
```
PermissionError: [Errno 13] Permission denied
```

**Why it fails:** Port 80 is a privileged port, and only root (UID 0) or processes with `CAP_NET_BIND_SERVICE` can bind to it.

#### Step 3: Verify It Works as Root

```bash
sudo python3 secure_server.py
```

**Expected Output:**
```
Starting server on port 80 as UID 0
Effective UID: 0
Process PID: 1234
...
Server running.
```

Stop the server with `Ctrl+C`.

**Question to Consider:** What's wrong with running the web server as root?

---

### Exercise 2: Granting Capabilities (10 minutes)

**Objective:** Use capabilities to allow the server to bind to port 80 without root privileges.

#### Step 1: Create a Capability-Enabled Python Binary

```bash
# Copy Python for this specific use case
sudo cp /usr/bin/python3 /usr/local/bin/webserver-python

# Grant the CAP_NET_BIND_SERVICE capability
sudo setcap 'cap_net_bind_service=+ep' /usr/local/bin/webserver-python
```

**Breaking down the command:**
- `cap_net_bind_service`: The capability to grant
- `+ep`: Add to Effective and Permitted sets
- `/usr/local/bin/webserver-python`: The target binary

#### Step 2: Verify the Capability

```bash
# Check capabilities on the binary
getcap /usr/local/bin/webserver-python
```

**Expected Output:**
```
/usr/local/bin/webserver-python cap_net_bind_service=ep
```

#### Step 3: Run the Server with Capabilities

```bash
# Run as regular user with capability-enabled Python
/usr/local/bin/webserver-python secure_server.py
```

**Expected Output:**
```
Starting server on port 80 as UID 1000
Effective UID: 1000
Process PID: 12345

Checking capabilities...
  CapInh: 0000000000000000
  CapPrm: 0000000000000400
  CapEff: 0000000000000400
  CapBnd: 000001ffffffffff
  CapAmb: 0000000000000000

Server running. Test with: curl http://localhost:80
Press Ctrl+C to stop.
```

**Success!** The server is running on port 80 as UID 1000 (non-root).

---

### Exercise 3: Testing the Server (5 minutes)

**Objective:** Verify the server works correctly while maintaining security boundaries.

#### Step 1: Test Basic Functionality

Open another terminal in the Docker container:

```bash
# In a new terminal/shell
docker exec -it capabilities-lab /bin/bash
su - student

# Test the web server
curl http://localhost/
```

**Expected Output:**
```
<!DOCTYPE HTML>
<html>
...
</html>
```

Check the server logs - they should show requests from UID 1000.

#### Step 2: Create a Test File

```bash
# Create a file to serve
echo "<h1>Hello from Capabilities Lab!</h1>" > ~/index.html

# Request it
curl http://localhost/index.html
```

---

### Exercise 4: Security Verification (10 minutes)

**Objective:** Verify that the capability-enabled process is still restricted by normal user permissions.

#### Step 1: Check Process Information

```bash
# Find the server process
ps aux | grep webserver-python

# Get detailed process information
PID=$(pgrep -f webserver-python)
echo "Server PID: $PID"

# Check process status
cat /proc/$PID/status | grep -E "Uid|Gid|Cap"
```

#### Step 2: Decode Capability Bitmask

```bash
# Decode the capability hex values
capsh --decode=0000000000000400
```

**Expected Output:**
```
0x0000000000000400=cap_net_bind_service
```

This confirms only `CAP_NET_BIND_SERVICE` is set.

#### Step 3: Verify File Access Restrictions

```bash
# Try to access a root-only file through the web server
# This should FAIL due to normal user permissions
curl http://localhost/../../../etc/shadow
```

**Expected Result:** Error or empty response. The server cannot read `/etc/shadow` because it runs as UID 1000.

#### Step 4: Check File Descriptors

```bash
# List open file descriptors
sudo ls -l /proc/$PID/fd/

# Check network connections
sudo netstat -tlnp | grep $PID
# or
sudo ss -tlnp | grep $PID
```

#### Step 5: Attempt Privileged Operations

Try operations that require other capabilities (should fail):

```bash
# Try to change system time (requires CAP_SYS_TIME)
# From within the server process context - this would fail

# Try to read dmesg (requires CAP_SYSLOG in some systems)
# The web server cannot do this
```

**Key Insight:** The process can ONLY bind to privileged ports. All other operations are restricted to normal user permissions.

---

### Exercise 5: Capability Management (5 minutes)

**Objective:** Practice managing capabilities.

#### Step 1: View All Capabilities

```bash
# List all available capabilities
capsh --print
```

#### Step 2: Remove Capability

```bash
# Stop the server first (Ctrl+C)

# Remove the capability
sudo setcap -r /usr/local/bin/webserver-python

# Verify removal
getcap /usr/local/bin/webserver-python
# (should return nothing)

# Try running the server again
/usr/local/bin/webserver-python secure_server.py
# Should fail with Permission denied
```

#### Step 3: Re-add Capability with Different Flags

```bash
# Add capability to only Permitted set
sudo setcap 'cap_net_bind_service=+p' /usr/local/bin/webserver-python

# Try running - will it work?
/usr/local/bin/webserver-python secure_server.py
```

**Question:** Why doesn't it work with only `+p`? (Hint: Check the difference between Permitted and Effective)

```bash
# Fix it: add to both Effective and Permitted
sudo setcap 'cap_net_bind_service=+ep' /usr/local/bin/webserver-python
```

---

## Expected Outcomes and Analysis

### What You Should Observe

1. **UID remains 1000** (non-root) throughout execution
2. **Capability bitmask** shows only `0x400` (CAP_NET_BIND_SERVICE)
3. **Server successfully binds** to port 80
4. **File access is restricted** to normal user permissions
5. **No other root privileges** are available to the process

### Capability Bitmask Reference

When you see:
```
CapPrm: 0000000000000400
CapEff: 0000000000000400
```

The `0x400` bit corresponds to:
- Bit 10 (counting from 0)
- Capability number 10 = `CAP_NET_BIND_SERVICE`

### Security Benefits

1. **Reduced attack surface**: If the web server is compromised, attackers gain limited privileges
2. **Principle of least privilege**: Process has only the minimum required capability
3. **Audit trail**: Capability usage can be monitored
4. **Defense in depth**: Even with one capability, the process cannot escalate to full root

---

## Cleanup

```bash
# Stop the server (Ctrl+C if still running)

# Remove capability-enabled binary
sudo rm /usr/local/bin/webserver-python

# Clean up test files
rm -f secure_server.py index.html

# Exit the container
exit
```

---

## Common Issues and Troubleshooting

### Issue 1: "getcap: command not found"

**Solution:**
```bash
sudo apt-get install libcap2-bin
```

### Issue 2: "Operation not permitted" when setting capabilities

**Solution:** Ensure you're running with sudo and the filesystem supports extended attributes.

In Docker:
```bash
docker run --cap-add=ALL ...
```

### Issue 3: Capabilities lost after program modification

**Explanation:** File capabilities are stored in extended attributes. If you modify the binary, capabilities are removed for security reasons.

**Solution:** Re-apply capabilities after any changes.

### Issue 4: Server still fails to bind after setcap

**Check:**
1. Verify capability is set: `getcap /path/to/binary`
2. Ensure you're using the correct binary
3. Check if another process is using port 80: `sudo netstat -tlnp | grep :80`

---

## Discussion Questions

1. **Security Trade-offs:**
   - What are the risks of granting capabilities to binaries?
   - How does this compare to using `sudo` for the entire process?

2. **Real-world Applications:**
   - What other services could benefit from capabilities?
   - When would you NOT want to use capabilities?

3. **Capability Management:**
   - Why might you want to grant capabilities to a copy of a binary rather than the original?
   - What happens if a capability-enabled binary is moved or copied?

4. **Attack Scenarios:**
   - If an attacker exploits a vulnerability in our web server, what can they do?
   - How do capabilities limit the damage?

---

## Additional Experiments

### Experiment 1: Multiple Capabilities

Try granting multiple capabilities:
```bash
sudo setcap 'cap_net_bind_service,cap_sys_time=+ep' /usr/local/bin/webserver-python
getcap /usr/local/bin/webserver-python
```

### Experiment 2: Ambient Capabilities

Research and test ambient capabilities for inherited capabilities:
```bash
# Requires more advanced setup
sudo setcap 'cap_net_bind_service=+eip' /usr/local/bin/webserver-python
```

### Experiment 3: Systemd Integration

Create a systemd service that uses capability-enabled binaries for production deployment.

---

## Key Takeaways

1. **Capabilities provide fine-grained privilege control** without full root access
2. **CAP_NET_BIND_SERVICE** allows binding to ports < 1024
3. **File capabilities** are set on binaries using `setcap`
4. **Process capabilities** can be inspected via `/proc/<pid>/status`
5. **Security is maintained**: Other permissions remain restricted
6. **Best practice**: Copy binaries before applying capabilities for isolation

---

## References and Further Reading

1. **Man Pages:**
   - `man capabilities(7)` - Overview of Linux capabilities
   - `man setcap(8)` - Set file capabilities
   - `man getcap(8)` - Get file capabilities
   - `man capsh(1)` - Capability shell wrapper

2. **Kernel Documentation:**
   - [Linux Capabilities](https://www.kernel.org/doc/html/latest/security/credentials.html)

3. **Security Resources:**
   - OWASP Principle of Least Privilege
   - CIS Benchmarks for Linux

4. **Tools:**
   - `libcap2-bin` package documentation
   - systemd capability integration

---

## Lab Completion Checklist

- [ ] Created and ran the web server script
- [ ] Observed permission denied error for normal user
- [ ] Applied `CAP_NET_BIND_SERVICE` capability to Python binary
- [ ] Successfully ran web server on port 80 as non-root
- [ ] Verified process capabilities using `/proc` filesystem
- [ ] Tested security boundaries (file access restrictions)
- [ ] Decoded capability bitmasks
- [ ] Practiced adding and removing capabilities
- [ ] Understood the difference between capability sets (Permitted, Effective, etc.)

---

## Assessment Questions

1. What command is used to grant capabilities to a binary?
2. What is the hexadecimal value for `CAP_NET_BIND_SERVICE` in the capability bitmask?
3. Why is it safer to run a web server with capabilities instead of as root?
4. What does the `+ep` flag mean in `setcap 'cap_net_bind_service=+ep'`?
5. Can a capability-enabled process read any file on the system? Why or why not?

---

**End of Lab Guide**

*Version: 1.0*
*Last Updated: 2025-11-12*
*Author: AI Workshop - Linux Security Series*
