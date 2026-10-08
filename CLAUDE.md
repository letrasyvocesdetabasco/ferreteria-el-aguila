# Instrucciones de Trabajo y Permisos para Claude Code

## Permisos de Git y GitHub
- **Autorización Completa:** Tienes autorización explícita y completa para realizar `git add`, `git commit`, `git push`, `git status`, `git pull` y `git diff` en todos los repositorios de este proyecto.
- **Flujo Autónomo:** Una vez que completes o verifiques cambios solicitados por el usuario, compila (`npm run build`), verifica que no haya errores y sube los cambios inmediatamente a la rama `main` mediante `git commit` y `git push`. No te detengas a pedir confirmación para subir los cambios a menos que el usuario lo solicite expresamente.
- **Credenciales del Sistema:** El sistema operativo ya tiene configuradas las credenciales de GitHub vía `git credential-helper store` (`~/.gitconfig` y `~/.git-credentials`). Los comandos `git push` funcionan de forma directa y autenticada sin necesidad de tokens manuales ni interacción de contraseña.

## Estructura de Proyectos y Repositorios
La carpeta principal `pagina web` aloja varios proyectos independientes, cada uno con su propio repositorio Git local y remoto:

1. **`letrasyvocesdetabasco/`**
   - Sitio oficial de la asociación civil Letras y Voces de Tabasco (Astro 5 + Tailwind CSS + Pagefind).
   - Despliegue automático: al hacer push a `origin main`, GitHub Actions (`.github/workflows/deploy.yml`) compila el sitio y lo publica en GitHub Pages (`gh-pages`).
   - Comando de compilación: `npm run build` (genera el bundle en `dist/` e indexa con Pagefind).
   - Servidor de previsualización local: `npm run preview` (habitualmente en el puerto 4321).
   - **IMPORTANTE:** Siempre ejecuta los comandos de git dentro de este directorio (`cd letrasyvocesdetabasco` o `git -C letrasyvocesdetabasco ...`). La carpeta padre no es un repositorio Git.

2. **`ferreteria_el_aguila/`**
   - Repositorio y catálogo web de Ferretería El Águila.
   - Ejecuta comandos de git dentro de su subdirectorio (`git -C ferreteria_el_aguila ...`).

3. **`estilo_molar/`**
   - Repositorio web de Estilo Molar.

## Buenas Prácticas
- Siempre prueba la compilación con `npm run build` antes de realizar un `git commit`.
- Utiliza mensajes de commit claros siguiendo el estándar convencional (`feat:`, `fix:`, `chore:`, `style:`).
- Al terminar cualquier tarea, informa al usuario sobre el estado de la subida a GitHub y los enlaces para ver los resultados.
