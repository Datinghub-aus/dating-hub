import os
import sys

# Define project structure
structure = {
    'static': ['css', 'js', 'images', 'charts'],
    'templates': {
        'home': ['partials/charts'],
        'blog': [],
        'tools': [],
        'directory': [],
        'legal': [],
        'emails': []
    },
    'core': [],
    'blog': [],
    'leads': [],
    'api': [],
    'media': [],
}

def create_dirs(base_path, structure):
    for folder, subfolders in structure.items():
        path = os.path.join(base_path, folder)
        os.makedirs(path, exist_ok=True)
        print(f"✓ Created: {path}")
        
        if isinstance(subfolders, dict):
            create_dirs(path, subfolders)
        elif isinstance(subfolders, list):
            for sub in subfolders:
                sub_path = os.path.join(path, sub)
                os.makedirs(sub_path, exist_ok=True)
                print(f"✓ Created: {sub_path}")

if __name__ == "__main__":
    base_dir = input("Enter project directory (or press Enter for current): ").strip()
    if not base_dir:
        base_dir = "."
    
    create_dirs(base_dir, structure)
    
    # Create essential files
    files_to_create = {
        'static/css/style.css': '/* Dating Hub Main CSS */\nbody { font-family: Inter, sans-serif; }',
        'static/js/main.js': '// Dating Hub Main JS\nconsole.log("Dating Hub 2026");',
        'requirements.txt': 'django>=4.2\npillow\ndjango-crispy-forms\ncrispy-tailwind\ndjango-allauth\ndjangorestframework\npython-dotenv',
        '.env': 'DEBUG=True\nSECRET_KEY=your-secret-key-here\nDATABASE_URL=sqlite:///db.sqlite3',
        '.gitignore': '__pycache__/\n*.pyc\n.env\n*.sqlite3\nstaticfiles/\nmedia/\n.DS_Store\nvenv/\n.env.local\n.env.development.local\n.env.test.local\n.env.production.local\n',
    }
    
    for file_path, content in files_to_create.items():
        full_path = os.path.join(base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        print(f"✓ Created: {full_path}")
    
    print("\n✅ Project structure created successfully!")
    print("Run: python manage.py startapp core blog leads api")
