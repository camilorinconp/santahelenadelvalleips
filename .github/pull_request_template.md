---
name: Plantilla de Pull Request
about: Plantilla estándar para todos los Pull Requests del proyecto.
title: ''
labels: ''
assignees: ''

---

### 1. ¿Qué problema o tarea resuelve este PR?
<!-- Describe de forma clara y concisa el objetivo. Si está relacionado con una tarea o issue, enlázalo aquí. Ej: "Resuelve el Issue #23" o "Implementa la Fase 2 del roadmap para Control de Cronicidad". -->


### 2. Resumen del Cambio
<!-- Describe a alto nivel qué se ha hecho. Ej: "Se ha creado el endpoint POST /control-cronicidad/diabetes-detalles/ y su lógica de servicio asociada." -->


### 3. Decisiones de Diseño y Arquitectura Tomadas
<!-- Esta es la sección más importante para la revisión del Equipo Asesor. Explica el "porqué" de tus decisiones. Ej: "Se decidió usar una tabla separada para los detalles de diabetes en lugar de añadir más columnas a `control_cronicidad` para seguir el patrón polimórfico definido en la documentación." -->


### 4. ¿Cómo se ha probado este cambio?
<!-- Describe los pasos para verificar que tu cambio funciona. Detalla las pruebas manuales realizadas y, sobre todo, las pruebas automatizadas que se han añadido. -->
- [ ] Se han añadido/actualizado pruebas unitarias en `tests/`.
- [ ] Se ha probado el endpoint manualmente con Postman/Swagger UI.
- [ ] Todas las pruebas existentes (`pytest`) pasan con éxito.


### 5. Checklist del Autor
- [ ] Mi código sigue las guías de estilo y las convenciones del proyecto.
- [ ] He añadido comentarios en el código, particularmente en las áreas más complejas.
- [ ] He actualizado la documentación relevante (ej. `README.md` o docstrings) si ha sido necesario.
- [ ] He verificado que no hay información sensible (claves, contraseñas) en el código.
