# Security Policy / سياسة الأمان

## Supported version
The latest `main` branch and current release line are supported.

## Security model
YAML Doctor processes files locally and does not require network access, credentials, or telemetry. YAML input is parsed with a loader derived from PyYAML `SafeLoader`; arbitrary Python object construction is not enabled. The formatter refuses to overwrite an existing output file unless `--force` is supplied.

Do not treat YAML Doctor as a sandbox for extremely large or adversarial resource-exhaustion payloads. Apply normal file-size/resource limits when processing untrusted content in automated services.

## Reporting
Please report security concerns privately through GitHub's security reporting facilities when available. Do not include credentials, private YAML, access tokens, or sensitive production data in public issues.

---

يعالج YAML Doctor الملفات محليًا ولا يحتاج إلى شبكة أو بيانات اعتماد. يستخدم محللًا مشتقًا من `SafeLoader` ولا يفعّل إنشاء كائنات Python عشوائية. لا تستخدم ملفات إنتاج حساسة في البلاغات العامة، وأبلغ عن المشكلات الأمنية بصورة خاصة عبر أدوات GitHub الأمنية عند توفرها.
