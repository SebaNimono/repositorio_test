# VulnShop — repositorio de pruebas para SSPILLOWY

> ⚠️ **Código vulnerable a propósito.** No usar en producción, no reutilizar fragmentos,
> no exponer a internet salvo como objetivo DAST temporal. Todas las claves son falsas.

Este repo existe para validar que los motores de [SSPILLOWY](https://sspillowy-sspy.vercel.app)
detectan lo que deben. Cada vulnerabilidad está plantada en un lugar conocido, así que el
resultado esperado de un escaneo es predecible.

## Qué debería detectar cada motor

| Motor | Archivo | Vulnerabilidades plantadas |
|---|---|---|
| **Semgrep** (SAST) | `app/app.py` | SQL injection, command injection, `eval`, `pickle.loads`, `yaml.load`, SSRF, XSS con `render_template_string`, `debug=True`, MD5 para contraseñas |
| **Semgrep** (SAST) | `web/server.js` | `eval` con input del usuario, `child_process.exec`, XSS reflejado, open redirect |
| **Gitleaks** (secretos) | `app/config.py`, `web/.env.production` | Clave privada RSA, API keys genéricas, JWT, contraseña de BD en URL |
| **Trivy** (SCA) | `requirements.txt`, `web/package-lock.json` | Flask 0.12.2, Jinja2 2.10, PyYAML 5.1, requests 2.19.1, urllib3 1.24.1, lodash 4.17.15, minimist 1.2.0 |
| **Trivy** (misconfig) | `Dockerfile` | Imagen base sin versión fija, corre como root, sin `HEALTHCHECK`, `ADD` en vez de `COPY` |
| **OWASP ZAP** (DAST) | app corriendo | Solo si se despliega y se configura `dast_url` en SSPILLOWY (ver abajo) |

## Uso en SSPILLOWY

1. En **Repositorios → Nuevo Repositorio**: URL `https://github.com/SebaNimono/repositorio_test`, rama `main`.
2. **Ejecutar Escaneo** con el perfil *Código completo* (Semgrep + Gitleaks + Trivy).
3. El gate debería quedar **BLOCKED** (hay críticos y secretos abiertos).

## Correr localmente (opcional, para DAST)

```bash
pip install -r requirements.txt
python app/app.py          # http://localhost:5000
```

Para ZAP hace falta una URL pública temporal (por ejemplo un túnel o un deploy efímero).
Bájala apenas termine el escaneo.
