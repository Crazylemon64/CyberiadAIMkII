import contextvars

# Ick, global state
botinstance = contextvars.ContextVar('bot')

