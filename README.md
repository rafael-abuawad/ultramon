# Ultramon 🐉

Un proyecto de NFT coleccionables inspirado en Pokémon, construido con Solidity y Ape Framework.

## 📋 Descripción

Ultramon es un contrato inteligente de NFT (ERC-721) que permite crear y coleccionar criaturas únicas llamadas "Ultramon". Cada Ultramon tiene propiedades únicas como HP, PC, D y una rara probabilidad de ser "shiny".

### 🎯 Características

- **NFTs Únicos**: Cada Ultramon es un token ERC-721 único
- **Propiedades Aleatorias**: HP, PC y D se generan aleatoriamente
- **Sistema Shiny**: 5% de probabilidad de obtener un Ultramon shiny
- **Tipos de Criaturas**: Charizard (Fuego) y Pikachu (Eléctrico)
- **Control de Propiedad**: Solo el propietario puede acuñar nuevos Ultramons

## 🏗️ Arquitectura del Contrato

### Estructuras de Datos

```solidity
struct Ultramon {
    string _name;    // Nombre del Ultramon
    string _type;    // Tipo (Fuego/Eléctrico)
    uint256 _hp;     // Puntos de vida (0-29)
    uint256 _pc;     // Puntos de combate (0-14)
    uint256 _d;      // Defensa (0-9)
    bool _shiny;     // ¿Es shiny?
}
```

### Propiedades de los Ultramons

- **HP (Puntos de Vida)**: 0-29
- **PC (Puntos de Combate)**: 0-14  
- **D (Defensa)**: 0-9
- **Shiny**: 5% de probabilidad (950-999 de 1000)

## 🚀 Instalación

### Prerrequisitos

- Python 3.8+
- [Ape Framework](https://docs.apeworx.io/)
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd ultramon
   ```

2. **Instalar dependencias**
   ```bash
   uv sync
   ```
    
3. **Instala los plguins de Apeworx**
   ```bash
   uv run ape plugins install .
   ```

4. **Verificar instalación**
   ```bash
   ape --version
   ```

## 🧪 Ejecutar Pruebas

Para ejecutar todas las pruebas:

```bash
ape test
```

Para ejecutar pruebas con más detalles:

```bash
ape test -v
```

Para ejecutar una prueba específica:

```bash
ape test -k test_safe_mint_success
```

### Cobertura de Pruebas

El proyecto incluye pruebas exhaustivas que cubren:

- ✅ Despliegue e inicialización del contrato
- ✅ Funcionalidad de acuñación (minting)
- ✅ Restricciones de propiedad
- ✅ Propiedades y rangos de los Ultramons
- ✅ Funcionalidad ERC-721 (transferencias, aprobaciones)
- ✅ Gestión de propiedad del contrato
- ✅ Casos edge y validaciones

## 📝 Uso del Contrato

### Despliegue

```solidity
// Desplegar el contrato
Ultramon ultramon = new Ultramon(msg.sender);
```

### Acuñar un Ultramon

```solidity
// Solo el propietario puede acuñar
ultramon.safeMint(destinatario);
```

### Consultar Propiedades

```solidity
// Obtener datos de un Ultramon
Ultramon memory ultramonData = ultramon.ultramons(tokenId);

// Acceder a propiedades específicas
string memory nombre = ultramonData._name;
string memory tipo = ultramonData._type;
uint256 hp = ultramonData._hp;
bool esShiny = ultramonData._shiny;
```

### Transferir NFT

```solidity
// Transferir un Ultramon
ultramon.transferFrom(desde, hacia, tokenId);
```

## 🔧 Configuración

### Archivo de Configuración (ape-config.yaml)

```yaml
name: ultramon

plugins:
  - name: solidity
  - name: optimism
  - name: etherscan

dependencies:
  - name: openzeppelin
    github: OpenZeppelin/openzeppelin-contracts
    version: 5.0.2
```

## 📁 Estructura del Proyecto

```
ultramon/
├── contracts/
│   └── Ultramon.sol          # Contrato principal
├── tests/
│   └── test_ultramon.py      # Suite de pruebas
├── ape-config.yaml           # Configuración de Ape
├── pyproject.toml           # Dependencias de Python
├── uv.lock                  # Lock file de dependencias
└── README.md               # Este archivo
```

## 🛠️ Desarrollo

### Compilar Contratos

```bash
ape compile
```

### Desplegar en Red Local

```bash
ape run deploy
```

### Interactuar con el Contrato

```bash
ape console
```

## 🔒 Seguridad

### Características de Seguridad

- **Control de Acceso**: Solo el propietario puede acuñar
- **Validaciones**: Verificación de direcciones válidas
- **Herencia Segura**: Uso de OpenZeppelin para estándares ERC-721
- **Pruebas Exhaustivas**: Cobertura completa de casos edge

### Auditoría

Antes de desplegar en producción, se recomienda:

1. Ejecutar todas las pruebas
2. Realizar auditoría de seguridad
3. Probar en redes de prueba
4. Verificar la configuración de red

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código

- Usar comentarios en español
- Seguir convenciones de Solidity
- Incluir pruebas para nuevas funcionalidades
- Documentar cambios importantes

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🐛 Reportar Bugs

Si encuentras un bug, por favor:

1. Revisa las issues existentes
2. Crea una nueva issue con:
   - Descripción detallada del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Información del entorno

## 📞 Contacto

Para preguntas o soporte:

- Crear una issue en GitHub
- Revisar la documentación de Ape Framework
- Consultar la documentación de OpenZeppelin

---

**¡Disfruta coleccionando Ultramons! 🎮**
