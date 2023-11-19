# DJChat

## Project Overview

This Django project is a server management system, enabling users to create servers, channels, and categories. The project also provides a Django REST framework API for retrieving server lists with various filtering options.

## Project Structure

### 1. Models

#### Category
- **Fields:** `name`, `description`, `icon`

#### Server
- **Fields:** `name`, `owner`, `category`, `description`, `members`

#### Channel
- **Fields:** `name`, `server`, `owner`, `topic`, `banner`, `icon`

### 2. File Uploads

- **Functions:**
  - `server_icon`, `server_banner`, `category_icon`: Define file upload paths.
- **Custom Validators:**
  - `validate_icon_size`, `validate_image_file_extension`: Validate file size and extension for server icons.

### 3. Signals and Deletion Handling

- `pre_delete` signals and custom methods handle file deletions when instances of `Category` and `Server` are deleted or their associated files are updated.

### 4. Serializers

- `ChannelSerializer`: Serializes `Channel` model instances.
- `ServerSerializer`: Serializes `Server` model instances, including related `Channel` instances and an optional count of members.

### 5. Views and API

- The project includes a Django REST framework ViewSet, `ServerListView`, handling server list-related operations.
- Custom query parameter handling for filtering servers by category, user, server ID, and more.

### 6. API Documentation

- Utilizes [drf-spectacular](https://github.com/tfranzel/drf-spectacular) for API schema generation.
- API documentation available at `/swagger/` and `/redoc/` endpoints.

### 7. Admin Interface

- Access the Django admin interface at `/admin/` for managing server categories, servers, and channels.

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

4. **Create a superuser for admin access:**
    ```bash
    python manage.py createsuperuser
    ```

5. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6. **Access the admin interface at `http://127.0.0.1:8000/admin/` to manage server categories, servers, and channels.**

## API Usage

1. Explore the API schema at `/swagger/` or `/redoc/` for detailed information on available endpoints and parameters.

2. Use the `/api/server/select/` endpoint to retrieve a list of servers with various filtering options.

    Example API Request:
    ```bash
    curl -X GET "http://127.0.0.1:8000/api/server/select/?category=example_category&qty=5&by_user=true&with_num_members=true" -H "accept: application/json"
    ```

## Contributing

1. **Fork the repository.**
2. **Create a new branch for your feature:** `git checkout -b feature/my-feature`.
3. **Commit your changes:** `git commit -m 'Add new feature'`.
4. **Push to the branch:** `git push origin feature/my-feature`.
5. **Open a pull request.**

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to contribute, report issues, or suggest improvements. Happy coding!
