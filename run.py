import sys
sys.path.insert(0, '/полный/путь/к/вашему_проекту')

from app import app

if __name__ == '__main__':
    app.run(debug=True)
