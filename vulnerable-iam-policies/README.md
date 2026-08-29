# vulnerable-iam-policies/

INTENTIONALLY dangerous IAM policy documents, added purely to demonstrate
the Parliament-based IAM scanner's detection capability. Same spirit as the
deliberate SAST fixtures in batch_script.py and spark-job/, and the DAST
fixtures in dast-target/. None of these policies are attached to any real
AWS role or user in this project.

- full-admin-policy.json           — unrestricted Action:*, Resource:* (total account compromise if attached)
- privilege-escalation-policy.json — classic iam:PassRole + ec2:RunInstances and iam:CreatePolicyVersion escalation paths
- assume-any-role-policy.json      — sts:AssumeRole on Resource:* (can pivot into any role in the account)
- unrestricted-iam-management-policy.json — iam:* (can create/modify/delete any user, role, or policy — full account takeover)
