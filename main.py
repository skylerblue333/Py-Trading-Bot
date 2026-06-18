import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class TradingSimulator:
    def __init__(self, initial_balance=10000):
        self.balance = initial_balance
        self.positions = 0
        self.history = []

    def evaluate_signal(self, price):
        # Simple mean reversion logic mock
        signal = random.choice(['BUY', 'SELL', 'HOLD'])
        return signal

    def execute_trade(self, signal, price):
        if signal == 'BUY' and self.balance >= price:
            self.balance -= price
            self.positions += 1
            logging.info(f"Executed BUY at ${price:.2f}. Balance: ${self.balance:.2f}")
        elif signal == 'SELL' and self.positions > 0:
            self.balance += price
            self.positions -= 1
            logging.info(f"Executed SELL at ${price:.2f}. Balance: ${self.balance:.2f}")

    def run_simulation(self, steps=10):
        current_price = 100.0
        logging.info(f"Starting simulation. Initial Balance: ${self.balance:.2f}")
        
        for i in range(steps):
            current_price += random.uniform(-5, 5)
            signal = self.evaluate_signal(current_price)
            self.execute_trade(signal, current_price)
            
        total_value = self.balance + (self.positions * current_price)
        logging.info(f"Simulation ended. Total Value: ${total_value:.2f}")

if __name__ == "__main__":
    bot = TradingSimulator()
    bot.run_simulation(20)