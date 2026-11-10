# Primary sources and further reading

Teaching pack prepared for w/c 9 November 2026. The links below support technical explanations. This pack's scenario, policy and exercises are original teaching material. Use the pinned dependencies for the lab; newer documentation may describe additional APIs.

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html): choice of password-hashing algorithm and cost.
- [argon2-cffi high-level API](https://argon2-cffi.readthedocs.io/en/stable/api.html): `PasswordHasher`, verification exceptions and rehash checks.
- [Flask-Login documentation](https://flask-login.readthedocs.io/en/latest/): user loading, login state and authentication decorators. Role policy remains application code.
- [Flask security considerations](https://flask.palletsprojects.com/en/stable/web-security/): cookie protections, CSRF context and template escaping.
- [Flask-WTF CSRF documentation](https://flask-wtf.readthedocs.io/en/latest/csrf/): global protection and hidden form tokens.
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html): least privilege and checks on each request.
- [OWASP IDOR Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html): object-specific access checks.
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html): server-side validity, logout, idle and absolute expiry.
- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html): token checks and SameSite limitations.
- [OWASP Multifactor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html): independent factors and recovery considerations.
- [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html): password length, factor properties, phishing resistance and account lifecycle. It is guidance in a particular assurance context, not a claim of compliance for this lab.
- [GitHub Codespaces templates](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/setting-up-your-repository/setting-up-a-template-repository-for-github-codespaces): repository-based environments.
- [classroom50 project](https://github.com/foundation50/classroom50) and [troubleshooting](https://github.com/foundation50/classroom50/blob/main/wiki/Troubleshooting.md): assignment templates, access and submission behaviour. Follow the configuration of your own classroom.
