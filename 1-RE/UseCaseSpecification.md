# Use-Case Flow Specification

## Use Case: Acknowledge Expiry Alert

**Use Case ID:** UC-005  
**Primary Actor:** SysAdmin  
**Secondary Actor:** Security Officer  
**System:** Domain & SSL Certificate Expiry Alert System  

### 1. Brief Description
This use case describes the process by which a SysAdmin acknowledges an automated alert regarding an impending domain or SSL certificate expiration, thereby halting further escalation.

### 2. Preconditions
- The system has performed a daily scan and detected a domain or SSL certificate approaching its expiration date (e.g., 30, 15, or 3 days).
- The system has triggered an Expiry Alert and sent a notification to the SysAdmin.
- The SysAdmin has an active account and is authorized to manage the affected domain/certificate.

### 3. Postconditions
- **Success Postcondition:** The alert is marked as "Acknowledged" in the system. The escalation timer is stopped, and the Security Officer is not notified. The system logs the acknowledgment timestamp and the user ID.
- **Failure Postcondition:** The alert remains active. The escalation timer continues to count down.

### 4. Main Success Scenario (Basic Flow)
1. The SysAdmin receives an Expiry Alert via email or SMS containing a unique link to the alert dashboard.
2. The SysAdmin clicks the link and accesses the system portal.
3. The system prompts the SysAdmin for authentication (Includes *Authenticate User*).
4. The SysAdmin enters valid credentials.
5. The system displays the details of the expiring domain or SSL certificate (e.g., Domain Name, Expiry Date, Days Remaining).
6. The SysAdmin clicks the "Acknowledge" button to confirm they are taking action to renew the asset.
7. The system updates the alert status to "Acknowledged" and stops the escalation timer.
8. The system logs the action and displays a success confirmation message to the SysAdmin.

### 5. Alternate Flows

**Alternate Flow 1: SysAdmin Fails to Acknowledge (Escalation - Extends Use Case)**
*At any point before step 6, if 48 hours pass since the alert was generated:*
1a. The system detects that the 48-hour escalation timer has expired without the alert being acknowledged.
2a. The system invokes the *Escalate Unacknowledged Alert* extension.
3a. The system automatically sends a high-priority escalation notification to the Security Officer, detailing the expiring asset and the unresponsive SysAdmin.
4a. The system updates the alert status to "Escalated".
5a. The use case ends.

**Alternate Flow 2: Authentication Failure**
*At step 4 of the Main Success Scenario:*
4a. The SysAdmin enters invalid credentials.
4b. The system displays an error message and prompts the user to try again or reset their password.
4c. If the SysAdmin fails to authenticate after 5 attempts, the account is temporarily locked, and the SysAdmin must contact support. The alert remains unacknowledged (escalation timer continues).
