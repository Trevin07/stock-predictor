from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from plotly.offline import plot
import plotly.graph_objects as go
import datetime 
from predictor import forecast_stock

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <html>
    <head>
        <title>AI Stock Forecast</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
            
            :root {{
                --primary: #00d4ff;
                --secondary: #0066ff;
                --dark: #0d1117;
                --light: #f8f9fa;
                --form-bg: rgba(13, 17, 23, 0.85);
                --header-height: 80px;
            }}
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Montserrat', sans-serif;
                color: var(--light);
                background-color: var(--dark);
                overflow-x: hidden;
            }}

            .background {{
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                z-index: -1;
            }}

            header {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: var(--header-height);
                background: rgba(13, 17, 23, 0.8);
                backdrop-filter: blur(10px);
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0 40px;
                box-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
                z-index: 100;
                border-bottom: 1px solid rgba(0, 212, 255, 0.2);
            }}

            .logo {{
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--light);
                text-decoration: none;
            }}

            .logo i {{
                color: var(--primary);
                font-size: 1.8rem;
            }}

            .nav-links {{
                display: flex;
                gap: 30px;
            }}

            .nav-links a {{
                color: var(--light);
                text-decoration: none;
                font-weight: 500;
                transition: all 0.3s ease;
                position: relative;
            }}

            .nav-links a:hover {{
                color: var(--primary);
            }}

            .nav-links a::after {{
                content: '';
                position: absolute;
                bottom: -5px;
                left: 0;
                width: 0;
                height: 2px;
                background: var(--primary);
                transition: width 0.3s ease;
            }}

            .nav-links a:hover::after {{
                width: 100%;
            }}

            .container {{
                position: relative;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: calc(var(--header-height) + 20px) 20px 80px; /* Adjusted from 40px to 20px */
                animation: fadeIn 1.5s ease-in;
            }}

            .hero {{
                text-align: center;
                margin-bottom: 40px;
                max-width: 800px;
            }}
            
            .logo-large {{
                font-size: 2.5rem;
                margin-bottom: 0px; /* Adjusted from 10px to 0px */
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 15px;
                animation: float 3s ease-in-out infinite;
            }}
            
            .logo-large i {{
                color: var(--primary);
                font-size: 3rem;
            }}

            h1 {{
                font-size: 3.5rem;
                margin-bottom: 20px;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
                background: linear-gradient(to right, var(--primary), var(--secondary));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: textGlow 2s ease-in-out infinite alternate;
                line-height: 1.2;
            }}

            .subtitle {{
                font-size: 1.3rem;
                margin-bottom: 30px;
                color: rgba(255, 255, 255, 0.8);
                max-width: 700px;
                line-height: 1.6;
            }}

            form {{
                background: var(--form-bg);
                padding: 50px;
                border-radius: 25px;
                box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
                backdrop-filter: blur(12px);
                width: 100%;
                max-width: 600px;
                text-align: center;
                border: 1px solid rgba(0, 212, 255, 0.2);
                transform: perspective(1000px) rotateX(0deg);
                transition: all 0.5s ease;
            }}
            
            form:hover {{
                transform: perspective(1000px) rotateX(5deg);
                box-shadow: 0 15px 35px rgba(0, 212, 255, 0.4);
            }}

            .form-group {{
                margin-bottom: 30px;
                text-align: left;
            }}

            label {{
                display: block;
                margin-bottom: 15px;
                font-size: 1.2rem;
                color: var(--primary);
                font-weight: 600;
            }}

            select {{
                width: 100%;
                padding: 18px;
                font-size: 1.1rem;
                border-radius: 12px;
                border: 2px solid rgba(0, 212, 255, 0.3);
                background-color: rgba(0, 0, 0, 0.5);
                color: var(--light);
                transition: all 0.3s ease;
                appearance: none;
                background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2300d4ff'%3e%3cpath d='M7 10l5 5 5-5z'/%3e%3c/svg%3e");
                background-repeat: no-repeat;
                background-position: right 20px center;
                background-size: 24px;
            }}

            select:focus {{
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.2);
            }}

            select:hover {{
                background-color: rgba(0, 0, 0, 0.7);
            }}

            .option-with-icon {{
                display: flex;
                align-items: center;
                padding: 12px 15px;
            }}

            .stock-logo {{
                width: 20px; 
                height: 20px; 
                margin-right: 10px; 
                border-radius: 4px;
                object-fit: contain;
            }}

            .btn {{
                width: 100%;
                padding: 18px;
                font-size: 1.2rem;
                font-weight: 600;
                border-radius: 12px;
                border: none;
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                color: var(--dark);
                cursor: pointer;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                z-index: 1;
            }}
            
            .btn::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, var(--secondary), var(--primary));
                transition: all 0.4s ease;
                z-index: -1;
            }}
            
            .btn:hover::before {{
                left: 0;
            }}
            
            .btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 10px 20px rgba(0, 212, 255, 0.3);
            }}
            
            .btn:active {{
                transform: translateY(1px);
            }}

            /* Footer styles */
            footer {{
                background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
                color: white;
                padding: 40px 20px;
                text-align: center;
                position: relative;
                z-index: 10;
            }}

            .footer-content {{
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                flex-direction: column;
                gap: 30px;
            }}

            .footer-logo {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                font-size: 1.5rem;
                margin-bottom: 20px;
            }}

            .footer-logo i {{
                color: var(--primary);
            }}

            .footer-links {{
                display: flex;
                justify-content: center;
                gap: 30px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }}

            .footer-links a {{
                color: rgba(255, 255, 255, 0.8);
                text-decoration: none;
                transition: color 0.3s ease;
            }}

            .footer-links a:hover {{
                color: var(--primary);
            }}

            .license {{
                background: rgba(0, 0, 0, 0.2);
                padding: 20px;
                border-radius: 10px;
                margin: 20px auto;
                max-width: 800px;
                font-size: 0.9rem;
                line-height: 1.6;
            }}

            .copyright {{
                color: rgba(255, 255, 255, 0.6);
                font-size: 0.9rem;
                margin-top: 20px;
            }}

            /* Animations */
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            @keyframes float {{
                0% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-10px); }}
                100% {{ transform: translateY(0px); }}
            }}
            
            @keyframes textGlow {{
                from {{ text-shadow: 0 0 10px rgba(0, 212, 255, 0.5); }}
                to {{ text-shadow: 0 0 20px rgba(0, 212, 255, 0.8); }}
            }}
            
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1); }}
            }}
            
            .pulse {{
                animation: pulse 2s infinite;
            }}

            /* Responsive adjustments */
            @media (max-width: 768px) {{
                h1 {{
                    font-size: 2.5rem;
                }}
                
                .subtitle {{
                    font-size: 1.1rem;
                }}
                
                form {{
                    padding: 30px;
                }}
                
                .nav-links {{
                    display: none;
                }}
                
                header {{
                    padding: 0 20px;
                }}
                
                .logo {{
                    font-size: 1.2rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="background"></div>
        
        <header>
            <a href="/" class="logo">
                <i class="fas fa-robot"></i>
                <span>QuantumPredict</span>
            </a>
            
        </header>
        
        <div class="container">
            <div class="hero">
                <div class="logo-large pulse">
                    <i class="fas fa-robot"></i>
                    <span>QuantumPredict AI</span>
                </div>
                <h1>Advanced Stock Price Predictions</h1>
                <p class="subtitle">
                    Harness the power of artificial intelligence to forecast stock prices with unprecedented accuracy. 
                    Our cutting-edge algorithms analyze market trends to provide you with reliable predictions.
                </p>
            </div>
            
            <form action="/predict">
                <div class="form-group">
                    <label for="symbol"><i class="fas fa-chart-line"></i> Select Stock Symbol</label>
                    <select name="symbol" id="symbol">
                        <option value="AAPL" class="option-with-icon">
                            <svg class="stock-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path fill="#A2AAAD" d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
                            </svg>
                            Apple (AAPL)
                        </option>
                        <option value="GOOGL" class="option-with-icon">
                            <svg class="stock-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path fill="#4285F4" d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/>
                            </svg>
                            Alphabet (GOOGL)
                        </option>
                        <option value="MSFT" class="option-with-icon">
                            <svg class="stock-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path fill="#F25022" d="M1 1h10v10H1z"/><path fill="#00A4EF" d="M1 13h10v10H1z"/><path fill="#7FBA00" d="M13 1h10v10H13z"/><path fill="#FFB900" d="M13 13h10v10H13z"/>
                            </svg>
                            Microsoft (MSFT)
                        </option>
                        <option value="AMZN" class="option-with-icon">
                            <svg class="stock-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path fill="#FF9900" d="M6.64 2.02c-.04-.25.18-.43.41-.36 1.9.6 6.36 2.02 7.8 2.47.38.12.55.54.33.86l-3.46 5.11c-.17.25-.5.3-.75.13l-2.9-1.92c-.3-.2-.7-.1-.85.23L4.1 15.1c-.15.33-.6.43-.9.2l-1.17-.8c-.3-.2-.35-.6-.15-.9l3.76-5.8V2.02zm9.5 1.5c.25 0 .5.1.7.3l1.83 1.83c.4.4.4 1 0 1.4l-1.83 1.83c-.4.4-1 .4-1.4 0l-1.83-1.83c-.4-.4-.4-1 0-1.4l1.83-1.83c.2-.2.45-.3.7-.3z"/>
                                <path fill="#000000" d="M12.23 15.26c-.4-.4-.4-1 0-1.4l1.83-1.83c.4-.4 1-.4 1.4 0l1.83 1.83c.4.4.4 1 0 1.4l-1.83 1.83c-.4.4-1 .4-1.4 0l-1.83-1.83z"/>
                            </svg>
                            Amazon (AMZN)
                        </option>
                        <option value="TSLA" class="option-with-icon">
                            <svg class="stock-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path fill="#E31937" d="M12 5.362c-3.486 0-6.313 2.827-6.313 6.313S8.514 17.988 12 17.988s6.313-2.827 6.313-6.313S15.486 5.362 12 5.362zm0 10.16c-2.123 0-3.847-1.724-3.847-3.847S9.877 8.83 12 8.83s3.847 1.724 3.847 3.847-1.724 3.847-3.847 3.847z"/>
                                <path fill="#E31937" d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18.313c-4.59 0-8.313-3.723-8.313-8.313S7.41 3.687 12 3.687 20.313 7.41 20.313 12 16.59 20.313 12 20.313z"/>
                            </svg>
                            Tesla (TSLA)
                        </option>
                        <option value="NFLX" class="option-with-icon">
                            <svg class="stock-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path fill="#E50914" d="M5.398 0v.006c-1.01.114-1.708.352-2.155.799C2.8 1.25 2.563 1.948 2.45 2.956H2.45v18.088c.114 1.008.352 1.706.799 2.153.447.448 1.145.684 2.153.798h.006V24H.021v-.006c-1.01-.114-1.708-.35-2.155-.798C-2.58 22.75-2.816 22.052-2.93 21.044H-2.93V2.956c.114-1.008.35-1.706.798-2.153C-1.684.355-.986.119.022.005V0h5.376zm13.177 6.552v4.2h-2.103v-4.2h-2.552v10.896h2.552v-4.2h2.103v4.2h2.552V6.552h-2.552zm6.314 0v10.896h5.107v-2.552h-2.555V6.552h-2.552z"/>
                            </svg>
                            Netflix (NFLX)
                        </option>
                        <option value="META" class="option-with-icon">
                            <svg class="stock-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path fill="#1877F2" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                            </svg>
                            Meta (META)
                        </option>
                        <option value="NVDA" class="option-with-icon">
                            <svg class="stock-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path fill="#76B900" d="M8.955 2.473a.3.3 0 0 1 .263.155l7.902 13.65a.3.3 0 0 1-.263.455h-3.08a.3.3 0 0 1-.263-.155L5.612 2.928a.3.3 0 0 1 .263-.455h3.08zm-6.343 0a.3.3 0 0 1 .263.155l3.08 5.32a.3.3 0 0 1-.263.455H2.473a.3.3 0 0 1-.263-.155l-1.54-2.66a.3.3 0 0 1 0-.31l1.54-2.66a.3.3 0 0 1 .263-.155h.139zm17.848 0a.3.3 0 0 1 .263.31l-.556 9.62a.3.3 0 0 1-.263.289h-2.223a.3.3 0 0 1-.263-.155l-4.173-7.21a.3.3 0 0 1 .263-.455h3.08a.3.3 0 0 1 .263.155l3.08 5.32a.3.3 0 0 0 .263.155h.139a.3.3 0 0 0 .263-.155l1.54-2.66a.3.3 0 0 0 0-.31l-1.54-2.66a.3.3 0 0 0-.263-.155h-.139z"/>
                            </svg>
                            NVIDIA (NVDA)
                        </option>
                        <option value="BTC-USD" class="option-with-icon">
                            <svg class="stock-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path fill="#F7931A" d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm0 22c-5.523 0-10-4.477-10-10S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/>
                                <path fill="#F7931A" d="M12.833 8.5h2.667v2.667h1.5V8.5h1.5V7h-1.5V4.333h-1.5V7h-2.667v1.5zm0 1.5v5.167h4.167v-1.5h-2.667V10h-1.5z"/>
                                <path fill="#F7931A" d="M10.333 9.833H7.5v1.5h2.833v1.5H7.5v1.5h2.833v1.5H6V8.333h4.333v1.5z"/>
                            </svg>
                            Bitcoin (BTC-USD)
                        </option>
                    </select>
                </div>
                <button type="submit" class="btn">
                    <i class="fas fa-chart-bar"></i> Generate AI Prediction
                </button>
            </form>
        </div>
        
        <footer>
            <div class="footer-content">
                <div class="footer-logo">
                    <i class="fas fa-robot"></i>
                    <span>QuantumPredict AI</span>
                </div>
                
                
                
                <div class="license">
                    <h3>MIT License</h3>
                    <p>
                        Permission is hereby granted, free of charge, to any person obtaining a copy
                        of this software and associated documentation files (the "Software"), to deal
                        in the Software without restriction, including without limitation the rights
                        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                        copies of the Software, and to permit persons to whom the Software is
                        furnished to do so, subject to the following conditions:
                    </p>
                    <p>
                        The above copyright notice and this permission notice shall be included in all
                        copies or substantial portions of the Software.
                    </p>
                </div>
                
                <div class="copyright">
                    &copy; <span id="year">{datetime.datetime.now().year}</span> Trevin Rodrigo. All rights reserved.
                </div>
            </div>
        </footer>
        
        <script>
            // Update year automatically
            document.getElementById('year').textContent = new Date().getFullYear();
        </script>
    </body>
    </html>
    """

@app.get("/predict", response_class=HTMLResponse)
def predict(symbol: str = Query(...)):
    # Dictionary mapping symbols to their SVG logos and names
    stock_info = {
        "AAPL": {
            "logo": f"""
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#A2AAAD" d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
                </svg>
            """,
            "name": "Apple"
        },
        "GOOGL": {
            "logo": f"""
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#4285F4" d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/>
                </svg>
            """,
            "name": "Alphabet"
        },
        "MSFT": {
            "logo": f"""
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#F25022" d="M1 1h10v10H1z"/><path fill="#00A4EF" d="M1 13h10v10H1z"/><path fill="#7FBA00" d="M13 1h10v10H13z"/><path fill="#FFB900" d="M13 13h10v10H13z"/>
                </svg>
            """,
            "name": "Microsoft"
        },
        "AMZN": {
            "logo": f"""
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#FF9900" d="M6.64 2.02c-.04-.25.18-.43.41-.36 1.9.6 6.36 2.02 7.8 2.47.38.12.55.54.33.86l-3.46 5.11c-.17.25-.5.3-.75.13l-2.9-1.92c-.3-.2-.7-.1-.85.23L4.1 15.1c-.15.33-.6.43-.9.2l-1.17-.8c-.3-.2-.35-.6-.15-.9l3.76-5.8V2.02zm9.5 1.5c.25 0 .5.1.7.3l1.83 1.83c.4.4.4 1 0 1.4l-1.83 1.83c-.4.4-1 .4-1.4 0l-1.83-1.83c-.4-.4-.4-1 0-1.4l1.83-1.83c.2-.2.45-.3.7-.3z"/>
                                <path fill="#000000" d="M12.23 15.26c-.4-.4-.4-1 0-1.4l1.83-1.83c.4-.4 1-.4 1.4 0l1.83 1.83c.4.4.4 1 0 1.4l-1.83 1.83c-.4.4-1 .4-1.4 0l-1.83-1.83z"/>
                            </svg>
            """,
            "name": "Amazon"
        },
        "TSLA": {
            "logo": f"""
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#E31937" d="M12 5.362c-3.486 0-6.313 2.827-6.313 6.313S8.514 17.988 12 17.988s6.313-2.827 6.313-6.313S15.486 5.362 12 5.362zm0 10.16c-2.123 0-3.847-1.724-3.847-3.847S9.877 8.83 12 8.83s3.847 1.724 3.847 3.847-1.724 3.847-3.847 3.847z"/>
                    <path fill="#E31937" d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18.313c-4.59 0-8.313-3.723-8.313-8.313S7.41 3.687 12 3.687 20.313 7.41 20.313 12 16.59 20.313 12 20.313z"/>
                </svg>
            """,
            "name": "Tesla"
        },
        "NFLX": {
            "logo": f"""
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#E50914" d="M5.398 0v.006c-1.01.114-1.708.352-2.155.799C2.8 1.25 2.563 1.948 2.45 2.956H2.45v18.088c.114 1.008.352 1.706.799 2.153.447.448 1.145.684 2.153.798h.006V24H.021v-.006c-1.01-.114-1.708-.35-2.155-.798C-2.58 22.75-2.816 22.052-2.93 21.044H-2.93V2.956c.114-1.008.35-1.706.798-2.153C-1.684.355-.986.119.022.005V0h5.376zm13.177 6.552v4.2h-2.103v-4.2h-2.552v10.896h2.552v-4.2h2.103v4.2h2.552V6.552h-2.552zm6.314 0v10.896h5.107v-2.552h-2.555V6.552h-2.552z"/>
                            </svg>
            """,
            "name": "Netflix"
        },
        "META": {
            "logo": f"""
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#1877F2" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                            </svg>
            """,
            "name": "Meta"
        },
        "NVDA": {
            "logo": f"""
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#76B900" d="M8.955 2.473a.3.3 0 0 1 .263.155l7.902 13.65a.3.3 0 0 1-.263.455h-3.08a.3.3 0 0 1-.263-.155L5.612 2.928a.3.3 0 0 1 .263-.455h3.08zm-6.343 0a.3.3 0 0 1 .263.155l3.08 5.32a.3.3 0 0 1-.263.455H2.473a.3.3 0 0 1-.263-.155l-1.54-2.66a.3.3 0 0 1 0-.31l1.54-2.66a.3.3 0 0 1 .263-.155h.139zm17.848 0a.3.3 0 0 1 .263.31l-.556 9.62a.3.3 0 0 1-.263.289h-2.223a.3.3 0 0 1-.263-.155l-4.173-7.21a.3.3 0 0 1 .263-.455h3.08a.3.3 0 0 1 .263.155l3.08 5.32a.3.3 0 0 0 .263.155h.139a.3.3 0 0 0 .263-.155l1.54-2.66a.3.3 0 0 0 0-.31l-1.54-2.66a.3.3 0 0 0-.263-.155h-.139z"/>
                            </svg>
            """,
            "name": "NVIDIA"
        },
        "BTC-USD": {
            "logo": f"""
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#F7931A" d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm0 22c-5.523 0-10-4.477-10-10S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/>
                    <path fill="#F7931A" d="M12.833 8.5h2.667v2.667h1.5V8.5h1.5V7h-1.5V4.333h-1.5V7h-2.667v1.5zm0 1.5v5.167h4.167v-1.5h-2.667V10h-1.5z"/>
                    <path fill="#F7931A" d="M10.333 9.833H7.5v1.5h2.833v1.5H7.5v1.5h2.833v1.5H6V8.333h4.333v1.5z"/>
                            </svg>
            """,
            "name": "Bitcoin"
        }
    }
    
    
    stock_data = stock_info.get(symbol, {
        "logo": f"""
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path fill="#999999" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
        """,
        "name": symbol
    })

    forecast, error = forecast_stock(symbol)

    if error:
        return f"""
        <html>
        <head>
            <title>Error</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
                body {{
                    font-family: 'Montserrat', sans-serif;
                    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                    color: white;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    flex-direction: column;
                }}
                .error-container {{
                    background: rgba(255, 0, 0, 0.1);
                    padding: 40px;
                    border-radius: 20px;
                    border: 1px solid rgba(255, 0, 0, 0.3);
                    max-width: 600px;
                    animation: shake 0.5s ease-in-out;
                }}
                .error-icon {{
                    font-size: 50px;
                    color: #ff4444;
                    margin-bottom: 20px;
                }}
                h1 {{
                    color: #ff4444;
                    margin-bottom: 20px;
                }}
                .btn {{
                    display: inline-block;
                    margin-top: 30px;
                    padding: 12px 25px;
                    background: linear-gradient(135deg, #00d4ff, #0066ff);
                    color: white;
                    text-decoration: none;
                    border-radius: 30px;
                    font-weight: bold;
                    transition: all 0.3s ease;
                }}
                .btn:hover {{
                    transform: translateY(-3px);
                    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                }}
                @keyframes shake {{
                    0%, 100% {{ transform: translateX(0); }}
                    20%, 60% {{ transform: translateX(-10px); }}
                    40%, 80% {{ transform: translateX(10px); }}
                }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h1>Prediction Error</h1>
                <p>{error}</p>
                <a href="/" class="btn">
                    <i class="fas fa-arrow-left"></i> Back to Home
                </a>
            </div>
        </body>
        </html>
        """

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast['ds'], 
        y=forecast['yhat'],
        name="Predicted Price",
        line=dict(color='#00d4ff', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.1)'
    ))
    
    fig.update_layout(
        title=f"{stock_data['name']} ({symbol}) -Price Forecast",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        plot_bgcolor='rgba(13, 17, 23, 0.9)',
        paper_bgcolor='rgba(13, 17, 23, 0.9)',
        font=dict(color='white'),
        hovermode='x unified',
        title_font_size=20,
        title_x=0.5,
        margin=dict(l=50, r=50, b=50, t=80, pad=10),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            showline=True,
            linecolor='rgba(255, 255, 255, 0.2)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            showline=True,
            linecolor='rgba(255, 255, 255, 0.2)'
        )
    )

    graph_html = plot(fig, output_type='div')

    return HTMLResponse(content=f"""
    <html>
    <head>
        <title>{stock_data['name']} Forecast</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
            
            body {{
                font-family: 'Montserrat', sans-serif;
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                color: white;
                margin: 0;
                padding: 0;
            }}
            
            .result-container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
                animation: fadeIn 1s ease-in;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            
            .header-content {{
                display: flex;
                align-items: center;
                justify-content: center; 
                gap: 15px; 
                margin-top: 20px; /* Adjusted from 0 to 20px */
            }}

            .stock-logo-large {{ 
                height: 55px; 
                width: 55px; 
            }}
            
            h1.graph-title {{ 
                font-size: 2.8rem; 
                margin-bottom: 0; 
                background: linear-gradient(to right, #00d4ff, #0066ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            
            .graph-container {{
                background: rgba(13, 17, 23, 0.8);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                margin-bottom: 40px;
                border: 1px solid rgba(0, 212, 255, 0.2);
            }}
            
            .btn {{
                display: inline-block;
                padding: 12px 25px;
                background: linear-gradient(135deg, #00d4ff, #0066ff);
                color: white;
                text-decoration: none;
                border-radius: 30px;
                font-weight: bold;
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }}
            
            .btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
            }}
            
            .btn i {{
                margin-right: 8px;
            }}
            
            footer {{
                background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
                color: white;
                padding: 40px 20px;
                text-align: center;
            }}
            
            .footer-content {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            
            .copyright {{
                color: rgba(255, 255, 255, 0.6);
                font-size: 0.9rem;
                margin-top: 20px;
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            @media (max-width: 768px) {{
                h1.graph-title {{
                    font-size: 2rem;
                    text-align: center; 
                }}
                .stock-logo-large {{
                    height: 40px;
                    width: 40px;
                }}
                .header-content {{
                    flex-direction: column; 
                    gap: 5px;
                }}
            }}
        </style>
    </head>x
    <body>
        <div class="result-container">
            <div class="header">
                <div class="header-content"> 
                    <div class="stock-logo-large">
                        {stock_data['logo']}
                    </div>
                    <h1 class="graph-title">{stock_data['name']} ({symbol}) Forecast</h1>
                </div>
                <p>AI-powered price prediction</p>
            </div>
            
            <div class="graph-container">
                {graph_html}
            </div>
            
            <div style="text-align: center;">
                <a href="/" class="btn">
                    <i class="fas fa-arrow-left"></i> Back to Home
                </a>
            </div>
        </div>
        
        <footer>
            <div class="footer-content">
                <div class="copyright">
                    &copy; {datetime.datetime.now().year} Trevin Rodrigo. QuantumPredict AI - MIT Licensed
                </div>
            </div>
        </footer>
    </body>
    </html>
    """)