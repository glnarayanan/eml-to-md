# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | Yes       |

Only the latest minor release receives security updates.

## Reporting a Vulnerability

If you discover a security vulnerability in eml-to-md, please report it responsibly.

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, please use [GitHub's private vulnerability reporting](https://github.com/glnarayanan/eml-to-md/security/advisories/new) or email **glnarayanan@gmail.com** with:

- A description of the vulnerability
- Steps to reproduce the issue
- The potential impact
- Any suggested fixes (optional)

### What to Expect

- **Acknowledgment** within 48 hours of your report
- **Status update** within 7 days with an assessment and remediation plan
- **Credit** in the release notes (unless you prefer to remain anonymous)

## Scope

This project processes `.eml` files, which are untrusted input by nature. Security concerns of particular interest include:

- **Path traversal** via crafted filenames (e.g., attachment names containing `../`)
- **Content injection** through malicious HTML email bodies
- **Denial of service** via pathologically large or deeply nested MIME structures
- **Information disclosure** from email headers or attachment metadata

## Out of Scope

- Vulnerabilities in upstream dependencies (e.g., `html2text`) — report those to the respective projects
- Issues requiring physical access to the machine running eml-to-md
