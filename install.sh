#!/bin/bash

echo "🚀 Setting up Employee Management System..."

# Step 1: Check Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 not installed. Please install it first."
    exit
fi

# Step 2: Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv1

# Step 3: Activate venv
echo "✅ Activating virtual environment..."
source venv1/bin/activate

# Step 4: Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Step 5: Install from requirements.txt
if [ -f requirements.txt ]; then
    echo "📥 Installing from requirements.txt..."
    pip install -r requirements.txt
else
    pip install django djangorestframework djangorestframework-simplejwt corsheaders
    echo "⚠️ No requirements.txt found!"
fi

# Step 6: Run migrations
echo "🔄 Applying migrations..."
python manage.py migrate

echo "✅ Setup complete!"
echo "👉 Run the server with: source venv/bin/activate && python manage.py runserver"
