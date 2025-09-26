# 📅 Rostering App

The **Rostering App** provides a simple CLI-based system for managing staff shifts and weekly reports.  

**Features:**
- **Admin** can schedule staff shifts and view reports.  
- **Staff** can view the combined roster and clock in/out of their shifts.  
- Weekly shift reports can be generated and reviewed.  

---

## Setup

Initialize the database and populate it with default data:
```bash
flask init
```

---

## Staff Commands

### Create a new staff member
```bash
flask staff create <username> <password>
```
**Example:**
```bash
flask staff create tom tompass
```

### View roster for the week
```bash
flask staff view_roster
```

### Clock staff in or out of a shift
```bash
flask staff clock <in|out> <shiftId>
```
**Example:**
```bash
flask staff clock in 4
```

---

## Admin Commands

### Create a new admin
```bash
flask admin create <username> <password>
```
**Example:**
```bash
flask admin create john johnpass
```

### Schedule a shift
```bash
flask admin schedule <staffId> <adminId> <startTime> <endTime>
```
**Example:**
```bash
flask admin schedule 1 1 "26/09/2025 09:00" "26/09/2025 17:00"
```

### List all reports
```bash
flask admin list_reports
```

### Create a new report
```bash
flask admin create_report
```

### View a report by ID
```bash
flask admin view_report <reportId>
```
**Example:**
```bash
flask admin view_report 2
```
