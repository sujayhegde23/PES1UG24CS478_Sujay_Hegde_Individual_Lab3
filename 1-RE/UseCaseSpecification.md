# Use-Case Flow Specification

**UC-005: Acknowledge Expiry Alert**
**Primary actor:** SysAdmin
**System:** Domain & SSL Certificate Expiry Alert System
**Student:** Sujay Hegde | PES1UG24CS478

## Preconditions

- An expiry alert exists and remains unacknowledged.
- SysAdmin has an active account and permission for the affected asset.

## Postconditions

**Success:** The system records the acknowledgment, actor, and timestamp and cancels pending escalation for this alert. Acknowledgment does not renew the domain or certificate.

**Failure:** Alert state is unchanged; any pending escalation deadline remains active.

## Main success scenario

1. SysAdmin opens the dashboard from an expiry notification.
2. The system authenticates the user and checks authorization for the asset.
3. The system displays the domain or endpoint, expiry date, and alert status.
4. SysAdmin selects Acknowledge.
5. The system atomically records acknowledgment and suppresses pending escalation for that alert.
6. The system records an audit entry and displays confirmation.

## Alternate flow - authentication failure

At step 2, invalid credentials cause the system to reject access and display a sign-in error. SysAdmin may retry with valid credentials, returning to step 2. If the user leaves, the use case ends without changing the alert.

**Related background behavior:** Independently of this user operation, the scheduler escalates an unacknowledged high-priority alert after 48 hours. This extends Handle Expiry Alert. It is not an alternate branch of an acknowledgment operation that never starts.
