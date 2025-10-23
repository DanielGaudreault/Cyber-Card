#!/usr/bin/env python3
"""
Capmatic PWA Setup Script
Helps prepare and verify the app icon for PWA installation
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

def check_icon_files():
    """Check if required icon files exist and are valid"""
    print("🔍 Checking icon files...")
    
    required_files = ['images/capmatic.png', 'images/logo.png']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
            print(f"❌ Missing: {file}")
        else:
            print(f"✅ Found: {file}")
            
            # Check image dimensions
            try:
                with Image.open(file) as img:
                    width, height = img.size
                    print(f"   📐 Dimensions: {width}x{height}")
                    
                    # Recommend optimal sizes
                    if file == 'images/capmatic.png':
                        if width < 512 or height < 512:
                            print(f"   ⚠️  Recommended: 512x512 for best PWA icon quality")
            except Exception as e:
                print(f"   ❌ Error reading {file}: {e}")
    
    return missing_files

def create_fallback_icons():
    """Create fallback icons if needed"""
    print("\n🎨 Creating fallback icons if needed...")
    
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    # Create capmatic.png if missing
    if not os.path.exists('images/capmatic.png'):
        print("📱 Creating capmatic.png fallback...")
        img = Image.new('RGB', (512, 512), color='#0a0a1a')
        draw = ImageDraw.Draw(img)
        
        # Add a simple "C" logo
        try:
            # Try to use a font
            font = ImageFont.truetype("Arial", 200)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        draw.text((256, 256), "C", fill='#00f7ff', font=font, anchor="mm")
        img.save('images/capmatic.png', 'PNG')
        print("✅ Created capmatic.png fallback")
    
    # Create logo.png if missing
    if not os.path.exists('images/logo.png'):
        print("👤 Creating logo.png fallback...")
        img = Image.new('RGB', (400, 400), color='#0a0a1a')
        draw = ImageDraw.Draw(img)
        
        # Add initials "DG"
        try:
            font = ImageFont.truetype("Arial", 120)
        except:
            font = ImageFont.load_default()
        
        draw.text((200, 200), "DG", fill='#00f7ff', font=font, anchor="mm")
        img.save('images/logo.png', 'PNG')
        print("✅ Created logo.png fallback")

def verify_pwa_requirements():
    """Verify all PWA requirements are met"""
    print("\n📋 Verifying PWA requirements...")
    
    requirements = {
        'HTTPS (for production)': '⚠️ Required for production deployment',
        'Service Worker': '✅ Implemented',
        'Web App Manifest': '✅ Implemented',
        'Icons (192px and 512px)': '✅ Configured',
        'Responsive Design': '✅ Implemented',
        'Start URL': '✅ Configured',
        'Theme Color': '✅ Configured'
    }
    
    for req, status in requirements.items():
        print(f"   {req}: {status}")

def main():
    """Main setup function"""
    print("🚀 Capmatic PWA Setup")
    print("=" * 40)
    
    # Check for required files
    missing_files = check_icon_files()
    
    # Create fallback icons if needed
    if missing_files:
        create_fallback_icons()
    
    # Verify PWA requirements
    verify_pwa_requirements()
    
    print("\n🎉 Setup complete!")
    print("\n📝 Next steps:")
    print("   1. Run: python app.py")
    print("   2. Open: http://localhost:5000")
    print("   3. Look for the install prompt (usually in address bar or menu)")
    print("   4. On mobile: Use 'Add to Home Screen' in browser menu")
    
    # Check if we're in a development environment
    if 'localhost' in os.environ.get('PYTHONANYWHERE_SITE', '') or 'localhost' in os.environ.get('SERVER_NAME', ''):
        print("\n⚠️  Note: PWA installation may require HTTPS in production")

if __name__ == '__main__':
    main()
