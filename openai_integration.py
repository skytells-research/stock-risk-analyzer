from typing import List, Dict, Any
import os
from flask import Flask, jsonify, request
from openai import OpenAI

class OpenAIIntegration:
    def __init__(self, app: Flask):
        self.app = app
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/.well-known/ai-plugin.json')
        def serve_plugin_manifest():
            return self.app.send_file('.well-known/ai-plugin.json')

        @self.app.route('/.well-known/openapi.yaml')
        def serve_openapi_spec():
            return self.app.send_file('.well-known/openapi.yaml')

    def format_analysis_for_openai(self, analysis: Dict[str, Any]) -> str:
        """Format the analysis results in a way that's easy for OpenAI to understand"""
        return f"""
        Analysis for {analysis['ticker']}:
        Risk Level: {analysis['risk_level']}
        Confidence: {analysis['confidence']:.2f}
        
        Technical Indicators:
        - Volatility: {analysis['indicators']['volatility']:.2f}
        - RSI: {analysis['indicators']['rsi']:.2f}
        - 50-day MA: {analysis['indicators']['ma50']:.2f}
        - 200-day MA: {analysis['indicators']['ma200']:.2f}
        
        Last Updated: {analysis['last_updated']}
        """

    async def handle_openai_request(self, messages: List[Dict[str, str]]) -> str:
        """Handle incoming requests from OpenAI"""
        try:
            # Extract the ticker from the user's message
            user_message = messages[-1]['content']
            
            # Use OpenAI to understand the request
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a stock market analysis assistant."},
                    {"role": "user", "content": user_message}
                ]
            )

            # Extract ticker symbols from the OpenAI response
            # This is a simplified example - you'd want more robust parsing
            tickers = self._extract_tickers(response.choices[0].message.content)
            
            # Get analysis for the tickers
            analyses = []
            for ticker in tickers:
                analysis = self._get_stock_analysis(ticker)  # Your existing analysis logic
                analyses.append(self.format_analysis_for_openai(analysis))

            return "\n\n".join(analyses)

        except Exception as e:
            return f"Error processing request: {str(e)}"

    def _extract_tickers(self, text: str) -> List[str]:
        """Extract stock ticker symbols from text"""
        # This is a simplified example
        # You'd want to implement more sophisticated ticker extraction
        words = text.split()
        tickers = [word.upper() for word in words if word.isupper() and len(word) <= 5]
        return tickers

    def _get_stock_analysis(self, ticker: str) -> Dict[str, Any]:
        """Get stock analysis using your existing analysis logic"""
        # This should integrate with your existing analysis code
        pass 