import pytest


def test_user_str(base_user):
    """Test the custom user model string representation"""
    assert base_user.__str__() == f"{base_user.username}"


def test_user_short_name(base_user):
    """Test that the user models get_short_name method works"""
    short_name = f"{base_user.username}"
    assert base_user.get_short_name() == short_name


def test_base_user_email_is_normalized(base_user):
    """Test that the new users email is normalized"""
    email = "person@API.COM"

    assert base_user.email == email.lower()


def test_super_user_email_is_normalized(super_user):
    """Test that an admin users email is normalized"""
    email = "person@API.COM"

    assert super_user.email == email.lower()


def test_super_user_is_not_staff(user_factory):
    """Test that an error is raised when an admin user has is_staff
    set to False"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email="", is_superuser=True, is_staff=False)
        assert str(err.value) == "Superusers must have is_staff=True"


def test_super_user_is_not_superuser(user_factory):
    """Test that an error is raised when an admin user has is_superuser
    set to False"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email="", is_superuser=False, is_staff=True)
        assert str(err.value) == "Superusers must have is_superuser=True"


def test_create_user_with_no_email(user_factory):
    """Test that creating a new user with no email address raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None, password="testpass")
        assert str(err.value) == "User Account: An email address is required"


def test_create_user_with_no_username(user_factory):
    """Test that creating a new user with no username raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email="person@api.com", username=None, password="testpass")
        assert str(err.value) == "Users must have a username"


def test_create_adminuser_with_no_email(user_factory):
    """Test that creating an admin user with no email address raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None, is_superuser=True, is_staff=True)
        assert str(err.value) == "Superuser Account: An email address is required"


def test_user_email_incorrect(user_factory):
    """Test that and error is raised when a non valid email is provided"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email="trial.com")
        assert str(err.value) == "You must provide a valid email address"
