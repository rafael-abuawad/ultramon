import ape
import pytest
from ape import reverts


@pytest.fixture
def owner(accounts):
    return accounts[0]


@pytest.fixture
def user(accounts):
    return accounts[1]


@pytest.fixture
def ultramon(owner, project):
    return project.Ultramon.deploy(owner, sender=owner)


def test_constructor(owner, project):
    """Prueba el despliegue e inicialización del contrato"""
    ultramon = project.Ultramon.deploy(owner, sender=owner)

    # Verificar nombre y símbolo del contrato
    assert ultramon.name() == "Ultramon"
    assert ultramon.symbol() == "ULTRA"

    # Verificar que el propietario está configurado correctamente
    assert ultramon.owner() == owner


def test_entries_initialization(ultramon):
    """Prueba que las entradas se inicialicen correctamente en el constructor"""
    # El contrato debe tener 2 entradas: Charizard y Pikachu
    # No podemos acceder directamente al array privado, pero podemos verificar a través del minting
    pass


def test_safe_mint_success(ultramon, owner, user):
    """Prueba el minting exitoso de un Ultramon"""
    # Acuñar un Ultramon
    tx = ultramon.safeMint(user, sender=owner)
    id = 0

    # Verificar que el token fue acuñado
    assert ultramon.ownerOf(id) == user
    assert ultramon.balanceOf(user) == 1

    # Verificar que el Ultramon fue creado
    ultramon_data = ultramon.ultramons(id)
    assert ultramon_data._name in ["Charizard", "Pikachu"]
    assert ultramon_data._type in ["Fuego", "Electrico"]
    assert ultramon_data._hp < 30  # Debe ser block.timestamp % 30
    assert ultramon_data._pc < 15  # Debe ser block.timestamp % 15
    assert ultramon_data._d < 10  # Debe ser block.timestamp % 10
    assert isinstance(ultramon_data._shiny, bool)

    # Verificar emisión de eventos (si los hay)
    assert len(tx.events) > 0


def test_safe_mint_only_owner(ultramon, user):
    """Prueba que solo el propietario puede acuñar"""
    with reverts():
        ultramon.safeMint(user, sender=user)


def test_multiple_mints(ultramon, owner, user):
    """Prueba múltiples acuñaciones a la misma dirección"""
    # Acuñar primer Ultramon
    ultramon.safeMint(user, sender=owner)
    assert ultramon.balanceOf(user) == 1
    assert ultramon.ownerOf(0) == user

    # Acuñar segundo Ultramon
    ultramon.safeMint(user, sender=owner)
    assert ultramon.balanceOf(user) == 2
    assert ultramon.ownerOf(1) == user


def test_mint_to_different_addresses(ultramon, owner, accounts):
    """Prueba acuñación a diferentes direcciones"""
    user1, user2 = accounts[1], accounts[2]

    # Acuñar a user1
    ultramon.safeMint(user1, sender=owner)
    assert ultramon.ownerOf(0) == user1
    assert ultramon.balanceOf(user1) == 1

    # Acuñar a user2
    ultramon.safeMint(user2, sender=owner)
    assert ultramon.ownerOf(1) == user2
    assert ultramon.balanceOf(user2) == 1


def test_ultramon_properties_range(ultramon, owner, user):
    """Prueba que las propiedades del Ultramon estén dentro de los rangos esperados"""
    ultramon.safeMint(user, sender=owner)
    ultramon_data = ultramon.ultramons(0)

    # Verificar rango de HP (0-29)
    assert 0 <= ultramon_data._hp < 30

    # Verificar rango de PC (0-14)
    assert 0 <= ultramon_data._pc < 15

    # Verificar rango de D (0-9)
    assert 0 <= ultramon_data._d < 10

    # Verificar que el nombre y tipo no estén vacíos
    assert len(ultramon_data._name) > 0
    assert len(ultramon_data._type) > 0


def test_ultramon_name_and_type_consistency(ultramon, owner, user):
    """Prueba que los nombres y tipos del Ultramon sean consistentes con las entradas"""
    ultramon.safeMint(user, sender=owner)
    ultramon_data = ultramon.ultramons(0)

    # Verificar que el nombre y tipo coincidan con los pares esperados
    if ultramon_data._name == "Charizard":
        assert ultramon_data._type == "Fuego"
    elif ultramon_data._name == "Pikachu":
        assert ultramon_data._type == "Electrico"
    else:
        pytest.fail(f"Nombre inesperado: {ultramon_data._name}")


def test_shiny_probability(ultramon, owner, user):
    """Prueba que la propiedad shiny sea booleana y tenga una probabilidad razonable"""
    ultramon.safeMint(user, sender=owner)
    ultramon_data = ultramon.ultramons(0)

    # Shiny debe ser un booleano
    assert isinstance(ultramon_data._shiny, bool)

    # La probabilidad debe ser alrededor del 5% (950-999 de 1000)
    # Esta es una verificación básica - en la práctica, querrías probar esto con muchas acuñaciones


def test_token_uri_functionality(ultramon, owner, user):
    """Prueba la función tokenURI (heredada de ERC721URIStorage)"""
    ultramon.safeMint(user, sender=owner)

    # tokenURI debe ser llamable (puede devolver cadena vacía si no está configurado)
    uri = ultramon.tokenURI(0)
    assert isinstance(uri, str)


def test_supports_interface(ultramon):
    """Prueba la función supportsInterface"""
    # Probar interfaz ERC721
    erc721_interface = "0x80ac58cd"
    assert ultramon.supportsInterface(erc721_interface)

    # Probar interfaz ERC165
    erc165_interface = "0x01ffc9a7"
    assert ultramon.supportsInterface(erc165_interface)


def test_erc721_transfer_functionality(ultramon, owner, accounts):
    """Prueba la funcionalidad básica de transferencia ERC721"""
    user1, user2 = accounts[1], accounts[2]

    # Acuñar a user1
    ultramon.safeMint(user1, sender=owner)

    # Transferir de user1 a user2
    ultramon.transferFrom(user1, user2, 0, sender=user1)

    # Verificar que cambió la propiedad
    assert ultramon.ownerOf(0) == user2
    assert ultramon.balanceOf(user1) == 0
    assert ultramon.balanceOf(user2) == 1


def test_approve_and_transfer(ultramon, owner, accounts):
    """Prueba la funcionalidad de aprobar y transferFrom"""
    user1, user2, user3 = accounts[1], accounts[2], accounts[3]

    # Acuñar a user1
    ultramon.safeMint(user1, sender=owner)

    # User1 aprueba a user2 para transferir el token 0
    ultramon.approve(user2, 0, sender=user1)

    # User2 transfiere el token 0 a user3
    ultramon.transferFrom(user1, user3, 0, sender=user2)

    # Verificar propiedad
    assert ultramon.ownerOf(0) == user3


def test_set_approval_for_all(ultramon, owner, accounts):
    """Prueba la funcionalidad setApprovalForAll"""
    user1, user2 = accounts[1], accounts[2]

    # Acuñar dos tokens a user1
    ultramon.safeMint(user1, sender=owner)
    ultramon.safeMint(user1, sender=owner)

    # User1 aprueba a user2 para todos los tokens
    ultramon.setApprovalForAll(user2, True, sender=user1)

    # Verificar aprobación
    assert ultramon.isApprovedForAll(user1, user2)


def test_mint_to_zero_address(ultramon, owner):
    """Prueba que acuñar a la dirección cero debe fallar"""
    zero_address = "0x0000000000000000000000000000000000000000"
    with reverts():
        ultramon.safeMint(zero_address, sender=owner)


def test_ultramon_data_persistence(ultramon, owner, user):
    """Prueba que los datos del Ultramon persistan después de la transferencia"""
    # Acuñar un Ultramon
    ultramon.safeMint(user, sender=owner)
    original_data = ultramon.ultramons(0)

    # Transferir el token
    new_owner = "0x1111111111111111111111111111111111111111"
    ultramon.transferFrom(user, new_owner, 0, sender=user)

    # Verificar que los datos siguen siendo los mismos
    transferred_data = ultramon.ultramons(0)
    assert transferred_data._name == original_data._name
    assert transferred_data._type == original_data._type
    assert transferred_data._hp == original_data._hp
    assert transferred_data._pc == original_data._pc
    assert transferred_data._d == original_data._d
    assert transferred_data._shiny == original_data._shiny


def test_ownership_transfer(ultramon, owner, user):
    """Prueba la funcionalidad de transferencia de propiedad"""
    # Transferir propiedad
    ultramon.transferOwnership(user, sender=owner)

    # Verificar nuevo propietario
    assert ultramon.owner() == user

    # El propietario anterior no debe poder acuñar
    with reverts():
        ultramon.safeMint(owner, sender=owner)

    # El nuevo propietario debe poder acuñar
    ultramon.safeMint(owner, sender=user)
    assert ultramon.ownerOf(0) == owner


def test_renounce_ownership(ultramon, owner):
    """Prueba renunciar a la propiedad"""
    # Renunciar a la propiedad
    ultramon.renounceOwnership(sender=owner)

    # Verificar que la propiedad fue renunciada
    assert ultramon.owner() == "0x0000000000000000000000000000000000000000"

    # No debe poder acuñar después de renunciar
    with reverts():
        ultramon.safeMint(owner, sender=owner)
