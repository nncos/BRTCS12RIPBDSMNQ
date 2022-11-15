# BRTCS12RIPBDSMNQ
> **B**asic **R**eal-**T**ime **C**lient-**S**ide **12**-bit **R**GB non-**I**nterlaced **P**article-**B**ased **D**isplay **S**ystem in **M**inecraft (Bedrock Edition) by **N**NCOS and **Q**azius

###### *The world's first (probably) live screen sharing program in Minecraft: Bedrock Edition!*

## How to use
1. Watch this demonstration video: https://www.youtube.com/watch?v=RH5J9twkyPs&t=16s
2. Download the resource packs from the 'resource packs' folder and add it to your word
3. Enter the world
4. Run the Python script 'BRTCS12RIPBDSMNQ.py' with an interpreter
5. Type the command '/connect localhost:19131' in your world and it should say 'Connection established...'
6. Teleport to (0, 300, 0) with '/tp 0 300 0'
7. Type 'play' to start the display
8. Other chat commands include:
   - 'stop': clears the display
   - 'invert': inverts the screen colour
   - 'normal': reverts the screen colour back to normal

## How it works
- Python script:
  1. Uses a websocket to establish a connection with your Minecraft world 
  2. When you send a message in Minecraft, a loop starts running
  3. Takes a screenshot and pixelates it
  4. Creates and sends a particle command to Minecraft for every pixel in the image
  5. Approx. every in-game tick (~0.1s), 100 particle commands are sent
  6. Display is fixed at coordinates (0, 300, 0)
- Resource pack:
  - 4096 custom particles (i.e. 4096 pixel colours)

##
Feel free to contact me to discuss any questions or comments

Discord: ᶜᵒˢ#4438

Credits: NNCOS and Qazius
