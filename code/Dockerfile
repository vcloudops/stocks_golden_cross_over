FROM python:3.11-slim

WORKDIR /app

# Install required packages
RUN pip install --no-cache-dir yfinance pandas matplotlib openpyxl

# Set environment variable to avoid matplotlib GUI issues
ENV MPLBACKEND=Agg

COPY app.py .

CMD ["python", "app.py"]
