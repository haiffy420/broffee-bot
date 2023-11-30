import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Define the menu of the coffee shop
menu = {
    "espresso": 2.0,
    "americano": 5.0,
    "cappucino": 6.0,
    "frappe": 7.0,
    "latte": 6.0,
    "mocha": 7.0,
    "tea": 2.0,
    "croissant": 3.0,
    "muffin": 2.5,
}

# User's cart to store ordered items
user_cart = {}


# Function to start the bot
def start(update, context):
    update.message.reply_text(
        "Welcome to our Broffee Shop! Here's our menu:\n\n"
        "1. Espresso - $2.0\n"
        "2. Americano - $5.0\n"
        "3. Cappucino - $6.0\n"
        "And much more!\n\n"
        "/menu - View menu items\n"
        "/order <item> <quantity> - Order items\n"
        "/cart - View your cart \n"
        "/dinein - Dine in\n"
        "/takeout - Takeout\n"
        "/delivery - Get delivery\n"
        "/end - End the conversation and/or reset your cart"
    )


# Function to display menu
def menu_items(update, context):
    update.message.reply_text(
        "Here's our menu:\n\n"
        "1. Espresso - $2.0\n"
        "2. Americano - $5.0\n"
        "3. Cappucino - $6.0\n"
        "4. Frappe - $7.0\n"
        "5. Latte - $6.0\n"
        "6. Mocha - $7.0\n"
        "7. Tea - $2.0\n"
        "8. Croissant - $3.0\n"
        "9. Muffin - $2.5\n\n"
    )


# Function to handle incoming orders
def order(update, context):
    user_input = " ".join(context.args).lower().split()

    if len(user_input) < 2:
        update.message.reply_text("Please provide both the item and quantity to order.")
        return

    item = user_input[0]
    quantity = int(user_input[1])

    if item not in menu:
        update.message.reply_text("Sorry, that item is not available in our menu.")
        return

    if quantity <= 0:
        update.message.reply_text("Please enter a valid quantity greater than zero.")
        return

    if item in user_cart:
        user_cart[item] += quantity
    else:
        user_cart[item] = quantity

    update.message.reply_text(f"{quantity} {item}(s) added to your cart!")


# Function to display the user's cart
def show_cart(update, context):
    if not user_cart:
        update.message.reply_text("Your cart is empty.")
        return

    total_cost = 0
    cart_text = "Your cart contains:\n"
    for item, quantity in user_cart.items():
        cost = menu[item] * quantity
        total_cost += cost
        cart_text += f"{item.capitalize()} - {quantity} - ${cost:.2f}\n"

    cart_text += f"\nTotal: ${total_cost:.2f}"
    update.message.reply_text(cart_text)


# Function to handle dining options
def dine_in(update, context):
    update.message.reply_text(
        "You've selected dine-in. Please find a seat and our staff will assist you shortly."
    )


# Function to handle takeout
def takeout(update, context):
    update.message.reply_text(
        "You've selected takeout. Your order will be prepared shortly for pickup."
    )


# Function to handle delivery
def delivery(update, context):
    update.message.reply_text(
        "You've selected delivery. Please provide your name and delivery destination.\n"
        "Example: /details John Doe, 123 Main Street"
    )


# Function to handle user details for delivery
def get_delivery_details(update, context):
    user_input = " ".join(context.args)

    if "," not in user_input:
        update.message.reply_text(
            "Please provide your name and delivery destination separated by a comma."
        )
        return

    name, destination = user_input.split(",", 1)
    update.message.reply_text(
        f"Thank you, {name.strip()}! Your order will be delivered to {destination.strip()} shortly."
    )


# Function to end conversation and reset cart
def end_conversation(update, context):
    update.message.reply_text(
        "Thank you for choosing our Coffee Shop! Your conversation has ended. "
        "Feel free to start a new one anytime."
    )
    user_cart.clear()  # Clear the user's cart


# Function to handle incoming messages
def echo(update, context):
    update.message.reply_text(
        "I'm just a simple coffee shop bot. You can order coffee, tea, croissant, muffin, or ask me anything!"
    )


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", menu_items))
    dp.add_handler(CommandHandler("order", order))
    dp.add_handler(CommandHandler("cart", show_cart))
    dp.add_handler(CommandHandler("dinein", dine_in))
    dp.add_handler(CommandHandler("takeout", takeout))
    dp.add_handler(CommandHandler("delivery", delivery))
    dp.add_handler(CommandHandler("details", get_delivery_details))
    dp.add_handler(CommandHandler("end", end_conversation))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
