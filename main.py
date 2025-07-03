if __name__ == '__main__':
    import uvicorn
    from src.app import app

    #uvicorn.run(app, host='0.0.0.0', port=80)
    uvicorn.run(app)