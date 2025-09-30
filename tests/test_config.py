"""Tests for configuration management."""

import os
import pytest
from unittest.mock import patch
from src.config import Config


class TestConfig:
    """Test cases for Config class."""

    @patch.dict(
        os.environ,
        {
            "EMAIL_ADDRESS": "test@example.com",
            "APP_PASSWORD": "testpassword",
            "RECIPIENT_EMAIL_LIST": "recipient1@test.com,recipient2@test.com",
        },
        clear=True,
    )
    def test_config_from_env_valid(self):
        """Test Config creation from valid environment variables."""
        config = Config.from_env()

        assert config.email_address == "test@example.com"
        assert config.app_password == "testpassword"
        assert config.recipient_emails == ["recipient1@test.com", "recipient2@test.com"]

    @patch.dict(os.environ, {}, clear=True)
    def test_config_from_env_missing_email(self):
        """Test Config creation with missing email address."""
        with pytest.raises(
            ValueError, match="EMAIL_ADDRESS and APP_PASSWORD must be set"
        ):
            Config.from_env()

    @patch.dict(
        os.environ,
        {
            "EMAIL_ADDRESS": "test@example.com",
            "APP_PASSWORD": "testpassword",
            "RECIPIENT_EMAIL_LIST": "",
        },
        clear=True,
    )
    def test_config_from_env_empty_recipients(self):
        """Test Config creation with empty recipient list."""
        with pytest.raises(ValueError, match="RECIPIENT_EMAIL_LIST must be set"):
            Config.from_env()

    def test_config_validation_invalid_email(self):
        """Test Config validation with invalid email."""
        config = Config(
            email_address="invalid-email",
            app_password="password",
            recipient_emails=["valid@email.com"],
        )

        with pytest.raises(ValueError, match="Invalid email address"):
            config.validate()

    def test_config_validation_invalid_recipient(self):
        """Test Config validation with invalid recipient email."""
        config = Config(
            email_address="valid@email.com",
            app_password="password",
            recipient_emails=["invalid-email"],
        )

        with pytest.raises(ValueError, match="Invalid recipient email"):
            config.validate()

    def test_config_validation_empty_password(self):
        """Test Config validation with empty password."""
        config = Config(
            email_address="valid@email.com",
            app_password="",
            recipient_emails=["valid@email.com"],
        )

        with pytest.raises(ValueError, match="App password cannot be empty"):
            config.validate()

    def test_config_validation_valid(self):
        """Test Config validation with valid data."""
        config = Config(
            email_address="valid@email.com",
            app_password="password",
            recipient_emails=["recipient1@email.com", "recipient2@email.com"],
        )

        # Should not raise any exception
        config.validate()
