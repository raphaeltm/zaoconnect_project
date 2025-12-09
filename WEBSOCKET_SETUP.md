# Django Channels WebSocket Cart Setup

## What Was Configured

### 1. **ASGI Configuration** (`zaoproject/asgi.py`)
- Fixed the ProtocolTypeRouter to properly route HTTP and WebSocket connections
- Added AuthMiddlewareStack for user authentication in WebSocket connections
- Imported the routing configuration from your app

### 2. **Routing** (`zaoapp/routing.py`)
- Created WebSocket URL pattern: `ws/cart/<room_name>/`
- Routes WebSocket connections to the CartConsumer

### 3. **Consumer** (`zaoapp/consumers.py`)
- Created `CartConsumer` class to handle WebSocket connections
- Supports real-time cart updates using Django Channels
- Handles three event types:
  - `cart_update`: Update cart display
  - `cart_item_added`: Item added notification
  - `cart_item_removed`: Item removed notification

### 4. **Settings** (`zaoproject/settings.py`)
- Added Channel Layers configuration (In-Memory for development)
- Set ASGI_APPLICATION to use the Channels ASGI app

### 5. **Template** (`zaoapp/templates/user/base.html`)
- Added WebSocket connection script to cart section
- Real-time cart UI updates
- Functions to send/receive cart data

## How It Works

1. **Connection**: When user loads the page, a WebSocket connection is established to `ws://localhost:8000/ws/cart/user/`

2. **Real-time Updates**: 
   - Cart count updates instantly
   - Item list updates without page reload
   - Total price recalculates in real-time

3. **Event Handling**:
   - `updateCartUI()` - Updates the cart display
   - `handleItemAdded()` - Handles item additions
   - `handleItemRemoved()` - Handles item removals

## Frontend Functions Available

```javascript
// Send a cart update
sendCartUpdate({
  count: 5,
  total: 2500.00,
  items: [...]
});

// Notify item added
notifyItemAdded({
  id: 1,
  name: 'Product Name',
  quantity: 2,
  subtotal: 500.00
});

// Notify item removed
notifyItemRemoved({
  id: 1,
  name: 'Product Name'
});
```

## Running the Server

For development, use Daphne (included with channels):

```bash
# With manage.py
python manage.py runserver

# Or with Daphne directly
daphne -b 0.0.0.0 -p 8000 zaoproject.asgi:application
```

## Production Notes

For production, replace the In-Memory Channel Layer with Redis:

```bash
pip install channels-redis
```

Then update `settings.py`:

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
```

## Next Steps

1. Connect cart add/remove buttons to the WebSocket functions
2. Create a backend view or API endpoint to handle cart operations
3. Broadcast cart updates to all connected users (group functionality)
4. Test in browser DevTools (Network > WS to see WebSocket traffic)
