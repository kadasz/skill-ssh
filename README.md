# opsdroid skill ssh

A skill interact with Linux servers by ssh commands

## Requirements
- `paramiko 2.7.1 or later`
- `SSH keys for authentication` 

## Configuration

Install this skill in your opsdroid by adding the following lines to your `configuration.yaml`:

```yaml
skills:
...
  ssh:
      path: /opt/opsdroid-skills/ssh/__init__.py
      user: 'admin'
      port: 22
      key: '/opt/opsdroid-skills/ssh/sshtask.key'
```

## Usage

### run on \<hostname> \<command>

Execute command on the remote server

```
  user: run on qnap uptime

  opsdroid: qnap - 08:19:35 up 425 days,  1:02,  2 users,  load average: 0.03, 0.11, 0.05
```
