## django-third-party-service


### Key Features

1. **API Key Management**: Create, enable/disable, and manage API keys.
2. **Scope Management**: Associate API keys with specific scopes and views.
3. **IP Whitelisting**: Whitelist specific IP addresses for API keys.
4. **Database Support**: Configurable for use with PostgreSQL.

### Custom Management Command: `update_views`

The project includes a custom Django management command named `update_views`. This command is designed to create or update all API views in the project and store them in the database. This enables administrators to add these views to specific scopes and create API keys for those scopes.

To use the `update_views` command, run the following:

```sh
python manage.py update_views
```

**Purpose of `update_views`:**
- **Automatic API View Management**: Automatically discovers all API views in the project and ensures they are up-to-date in the database.
- **Scope Association**: Facilitates the association of API views with specific scopes, enabling fine-grained control over which APIs third-party services can access.
- **Security and Access Control**: Ensures that third-party services can only access the APIs that they are explicitly granted access to via API keys and their associated scopes.

### Usage

The primary usage involves managing API keys and their permissions via the Django admin interface or potentially via an API (if implemented).

1. **Add API Views to Scopes**: After running the `update_views` command, API views can be added to specific scopes in the admin interface.
2. **Create API Keys for Scopes**: Create API keys and associate them with the desired scopes, limiting access to specific APIs for third-party services.

