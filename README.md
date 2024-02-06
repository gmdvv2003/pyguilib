# pyguilib

pyguilib is a free and open-source cross-platform graphical user interface library for the multimedia applications development library [Pygame](https://github.com/pygame/pygame). This library aims to simplify the process of creating and managing user interfaces by providing an abstraction inspired by Roblox's interface system.

![alt text](https://i.imgur.com/5DgiDhz.png)

Before installing pyguilib, ensure that Python is installed on your machine. You can check this by running the following command in your terminal or command prompt:
```
python --version
```
If Python is not installed, you can download and install it from the official

Once Python is installed, you can proceed to install pyguilib using the following command:
```
pip install pyguilib
```

![alt text](https://i.imgur.com/NkftzMs.png)
<details>
  <summary>Components</summary>ㅤ<!---Invisible Space--->
  
  ![alt text](https://i.imgur.com/kCrHoVZ.png)
  
  <i>PyGuiInstance represents the very core of every component. Containing the base properties and methods for all the components.</i>
  * <details>
    <summary>Constructor</summary>

    ```python
    PyGuiInstance(
        draw_order = 0,
        background_color = Color(140, 140, 140),
        background_transparency = 255,
        border_color = Color(0, 0, 0),
        border_size = 0,
        position = UDim2(0, 0, 0, 0),
        size = UDim2(1, 0, 1, 0),
        anchor_point = Vector2(0, 0),
        layout_order = 0,
        parent = None,
        name = None,
        **_,
      )
    ```
    + `draw_order`: (int): The order in which the GUI instance is drawn.
    + `background_color` (Color): The background color of the GUI instance.
    + `background_transparency` (float): The transparency of the GUI instance background.
    + `border_color` (Color): The color of the GUI instance border.
    + `border_size` (int): The size of the GUI instance border.
    + `position` (UDim2): The position of the GUI instance relative to its parent.
    + `size` (UDim2): The size of the GUI instance relative to its parent.
    + `anchor_point` (Vector2): The anchor point around which the GUI instance is positioned and scaled.
    + `layout_order` (int): The order in which the GUI instance is laid out.
    + `parent` (Optional[PyGuiInstance]): The parent GUI instance.
    + `name` (str): The name of the GUI instance.
    + `**_`: Additional keyword arguments.
    </details>
  * <details>
    <summary>Methods</summary>
    
    + `build()` -> `PyGuiInstance`: Build the GUI instance and add it to the parent.
    + `get_property_changed_signal(property_name: str)` -> `PyGuiSignal`: Get the signal for property changes.
    + `update(events: List[Event])`: Update the GUI instance based on events.
    + `clear()`: Clear the GUI instance.
    + `draw()`: Draw the GUI instance.
    </details>
  * <details>
    <summary>Properties</summary>
    
    + `visible` (bool): Property indicating whether the GUI instance is visible.
    + `draw_order` (int): Property indicating the draw order of the GUI instance.
    + `background_color` (Color): Property indicating the background color of the GUI instance.
    + `background_transparency` (float): Property indicating the transparency of the GUI instance background.
    + `border_color` (Color): Property indicating the border color of the GUI instance.
    + `border_size` (int): Property indicating the border size of the GUI instance.
    + `position` (UDim2): Property indicating the position of the GUI instance.
    + `absolute_position` (Vector2): Property indicating the absolute position of the GUI instance.
    + `size` (UDim2): Property indicating the size of the GUI instance.
    + `absolute_size` (Vector2): Property indicating the absolute size of the GUI instance.
    + `anchor_point` (Vector2): Property indicating the anchor point of the GUI instance.
    + `layout_order` (int): Property indicating the layout order of the GUI instance.
    + `parent` (Optional[PyGuiInstance]): Property indicating the parent GUI instance.
    + `name` (str): Property indicating the name of the GUI instance.
    + `BLOCKING_SCREEN_BUFFER_UPDATE` (int): Property to block screen buffer updates.
    </details>

  ---
    
  ![alt text](https://i.imgur.com/ljNurDd.png)
  
  <i>Frame class representing a container with layout capabilities.</i>
  * Inherits from:
    `PyGuiInstance`
    `PyGuiLayoutContainer`
  * <details>
    <summary>Constructor</summary>
    
    ```python
    Frame(**kwags)
    ```
    + `**kwags`: Additional keyword arguments used by PyGuiInstance and/or PyGuiLayoutContainer.
    </details>

  ---

  ![alt text](https://i.imgur.com/7Y40q1w.png)
  
  <i>ImageLabel class representing an image label component.</i>
  * Inherits from:
    `PyGuiInstance`
  * <details>
    <summary>Constructor</summary>
    
    ```python
    ImageLabel(
        image_color = Color(255, 255, 255),
        image_transparency = 255,
        **kwags
      )
    ```
    + `image_color`: (Color): The image color.
    + `image_transparency` (int): The image transparency.
    + `**kwags`: Additional keyword arguments used by PyGuiInstance.
    </details>

  ---

  ![alt text](https://i.imgur.com/0mwk4Ri.png)
  
  <i>TextBox class represents a GUI component for text input.</i>
  * Inherits from:
    `TextLabel`
    `PyGuiInstance`
  * <details>
    <summary>Constructor</summary>
    
    ```python
    TextBox(
        placeholder_text = "TextBox",
        placeholder_text_color = Color(255, 0, 0),
        placeholder_text_transparency = 255,
        text_font = Font("Arial", self.text_size),
        text_editable = True,
        clear_text_on_focus_lost = False,
        selection_color = Color(255, 255, 255),
        selection_transparency = 170,
        cursor_blink_interval = 0.5,
        cursor_appeareance = function(text_box: TextBox) -> Surface,
        **kwags
      )
    ```
    + `placeholder_text` (str): The current placeholder text.
    + `placeholder_text_color` (Color): The current color of the placeholder text.
    + `placeholder_text_transparency` (int): The current transparency of the placeholder text.
    + `placeholder_text_font` (pygame.font.Font): The current font used for the placeholder text.
    + `text_editable` (bool): True if the text is editable, False otherwise.
    + `clear_text_on_focus_lost` (bool): True if text should be cleared on focus lost, False otherwise.
    + `selection_start` (int): The starting index of the text selection.
    + `selection_end` (int): The ending index of the text selection.
    + `cursor_position` (int): The current cursor position.
    + `**kwags`: Additional keyword arguments used by TextLabel and/or PyGuiInstance.
    </details>
  * <details>
    <summary>Methods</summary>
    
    + `is_focused()`: Check if the TextBox is currently focused.
    + `capture_focus()`: Capture focus for the TextBox.
    + `release_focus(enter_pressed: bool = False)`: Release focus for the TextBox.
    + `placeholder_text()`: Get or set the placeholder text.
    + `placeholder_text_color()`: Get or set the color of the placeholder text.
    + `placeholder_text_transparency()`: Get or set the transparency of the placeholder text.
    + `placeholder_text_font()`: Get or set the font used for the placeholder text.
    + `text_editable()`: Get or set the flag indicating whether the text is editable.
    + `clear_text_on_focus_lost()`: Get or set the flag indicating whether to clear text on focus lost.
    + `selection_start()`: Get the starting index of the text selection.
    + `selection_end()`: Get the ending index of the text selection.
    + `cursor_position()`: Get the current cursor position in the text.
    </details>
  * <details>
    <summary>Properties</summary>
    
    + `placeholder_text` (str): The current placeholder text.
    + `placeholder_text_color` (Color): The current color of the placeholder text.
    + `placeholder_text_transparency` (int): The current transparency of the placeholder text.
    + `placeholder_text_font` (pygame.font.Font): The current font used for the placeholder text.
    + `text_editable` (bool): True if the text is editable, False otherwise.
    + `clear_text_on_focus_lost` (bool): True if text should be cleared on focus lost, False otherwise.
    + `selection_start` (int): The starting index of the text selection.
    + `selection_end` (int): The ending index of the text selection.
    + `cursor_position` (int): The current cursor position.
    </summary>

  ---
      
  ![alt text](https://i.imgur.com/Y9CbVGb.png)
  
  <i>TextLabel class represents a GUI component for displaying text.</i>
  * Inherits from:
    `PyGuiInstance`
  * <details>
    <summary>Constructor</summary>

    ```python
    TextLabel(
        text = "TextLabel",
        text_color = Color(255, 255, 255),
        text_transparency = 255,
        text_size = 16,
        text_font = Font("Arial", self.text_size),
        border_color = Color(0, 0, 0),
        border_size = 1,
        text_x_alignment = TextXAlignment.CENTER,
        text_y_alignment = TextYAlignment.CENTER,
        **kwags
      )
    ```
    + `text` (str): The text content.
    + `text_color` (Color): The text color.
    + `text_transparency` (int): The text transparency.
    + `text_size` (int): The text size.
    + `text_font` (pygame.font.Font): The text font.
    + `text_border_color` (Color): The text border color.
    + `text_border_size` (int): The text border size.
    + `text_x_alignment` (TextXAlignment): The text horizontal alignment.
    + `text_y_alignment` (TextYAlignment): The text vertical alignment.
    + `**kwags`: Additional keyword arguments used by PyGuiInstance.
    </details>
  * <details>
    <summary>Methods</summary>
  
    + `text_position()`: Calculates the position of the text based on alignment.
    + `text_bounds()`: Gets the bounding box of the text.
    </details>
  * <details>
    <summary>Properties</summary>

    + `text` (str): The text content.
    + `text_color` (Color): The text color.
    + `text_transparency` (int): The text transparency.
    + `text_size` (int): The text size.
    + `text_font` (pygame.font.Font): The text font.
    + `text_border_color` (Color): The text border color.
    + `text_border_size` (int): The text border size.
    + `text_x_alignment` (TextXAlignment): The text horizontal alignment.
    + `text_y_alignment` (TextYAlignment): The text vertical alignment.
    </details>
  * <details>
    <summary>Enums</summary>

    + `TextXAlignment`
      + LEFT: Align text to the left.
      + CENTER: Center-align text.
      + RIGHT: Align text to the right.
    + `TextYAlignment`
      + TOP: Align text to the top.
      + CENTER: Center-align text vertically.
      + BOTTOM: Align text to the bottom.
    </details>

  ---

  ![alt text](https://i.imgur.com/JtoU5Co.png)
  
  <i>VideoLabel class represents a GUI component for displaying a GIF.</i>
  * Inherits from:
    `PyGuiInstance`
  * <details>
    <summary>Constructor</summary>

    ```python
    VideoLabel(
        gif_playback_speed = 1,
        gif_color = Color(255, 255, 255),
        gif_transparency = 255,
        **kwags
      )
    ```
    + `gif_playback_speed` (str): The GIF playback speed.
    + `gif_color` (Color): The GIF color.
    + `gif_transparency` (int): The GIF transparency.
    + `**kwags`: Additional keyword arguments used by PyGuiInstance.
    </details>
  * <details>
    <summary>Methods</summary>
  
    + `pause()`: Placeholder method for pausing the GIF.
    + `resume()`: Placeholder method for resuming the GIF.
    </details>
  * <details>
    <summary>Properties</summary>

    + `current_gif_frame` (int): Index of the current GIF frame.
    + `gif_playback_speed` (int): The GIF playback speed.
    + `gif_color` (Color): The GIF color.
    + `gif_transparency` (int): The GIF transparency.
  </details>
</details>

<details>
  <summary>Layouts</summary>ㅤ<!---Invisible Space--->

  ![alt text](https://i.imgur.com/b4YVsPb.png)

  <i>PyGuiLayoutStyle class represents a layout style for PyGuiInstance.</i>
  * <details>
    <summary>Constructor</summary>

    ```python
    PyGuiLayoutStyle(
        on_layout_instance_child_added = lambda: None,
        on_layout_instance_child_removed = lambda: None,
        on_layout_applied = lambda: None,
        on_layout_removed = lambda: None,
        layout_order_manager = lambda: None,
        **kwags
      )
    ```
    + `on_layout_instance_child_added (Optional[Callable[[Any], Any]])`: Callback for child addition to the layout.
    + `on_layout_instance_child_removed (Optional[Callable[[Any], Any]])`: Callback for child removal from the layout.
    + `on_layout_applied (Optional[Callable[[Any], Any]])`: Callback for when the layout is applied.
    + `on_layout_removed (Optional[Callable[[Any], Any]])`: Callback for when the layout is removed.
    + `layout_order_manager (Optional[Callable[[Any], Any]])`: Callback for managing the layout order.
    + `**kwargs`: Additional keyword arguments.
    </details>
  * <details>
    <summary>Properties</summary>

    + `instance` (PyGuiInstance): The associated PyGuiInstance.
    + `horizontal_alignment` (HorizontalAlignment): The horizontal alignment of child instances.
    + `vertical_alignment` (VerticalAlignment): The vertical alignment of child instances.
    + `fill_direction` (FillDirection): The fill direction for child instances.
    + `sort_order` (SortOrder): The sorting order for child instances.
    </details>
  * <details>
    <summary>Enums</summary>

    + `HorizontalAlignment`
      + LEFT: Aligns child instances to the left of the parent instance.
      + CENTER: Aligns child instances to the center of the parent instance.
      + RIGHT: Aligns child instances to the right of the parent instance.
    + `VerticalAlignment`
      + TOP: Aligns child instances to the top of the parent instance.
      + CENTER: Aligns child instances to the center of the parent instance.
      + BOTTOM: Aligns child instances to the bottom of the parent instance.
    + `FillDirection`
      + HORIZONTAL: Aligns child instances horizontally.
      + VERTICAL: Aligns child instances vertically.
    + `SortOrder`
      + NAME: Sorts child instances by name.
      + LAYOUT_ORDER: Sorts child instances by layout order.
      + CUSTOM: Sorts child instances by custom order.
    </details>
  ___

  ![alt text](https://i.imgur.com/Z62Cr8i.png)

  <i>PyGuiListLayout class represents a list layout style for a PyGui instance.</i>
  * Inherits from:
    `PyGuiLayoutStyle`
  * <details>
    <summary>Constructor</summary>

    ```python
    PyGuiListLayout(
        horizontal_padding = UDim(0, 0),
        vertical_padding = UDim(0, 0),
        top_margin = Udim(0, 0),
        bottom_margin = Udim(0, 0),
        left_margin = Udim(0, 0),
        right_margin = Udim(0, 0),
        **kwags
      )
    ```
    + `horizontal_padding (UDim)`: The horizontal padding for child instances.
    + `vertical_padding (UDim)`: The vertical padding for child instances.
    + `top_margin (UDim)`: The top margin for child instances.
    + `bottom_margin (UDim)`: The bottom margin for child instances.
    + `left_margin (UDim)`: The bottom margin for child instances.
    + `right_margin (UDim)`: The left margin for child instances.
    + `**kwargs`: Additional keyword arguments used by PyGuiLayoutStyle.
    </details>
  * <details>
    <summary>Properties</summary>

    + `horizontal_padding (UDim)`: The horizontal padding for child instances.
    + `vertical_padding (UDim)`: The vertical padding for child instances.
    + `top_margin (UDim)`: The top margin for child instances.
    + `bottom_margin (UDim)`: The bottom margin for child instances.
    + `left_margin (UDim)`: The bottom margin for child instances.
    + `right_margin (UDim)`: The left margin for child instances.
    </details>
</details>

<details>
  <summary>Services</summary>ㅤ<!---Invisible Space--->

  ![alt text](https://i.imgur.com/5D6oHUf.png)
  
  <i>TweenService is used as an interface to directly apply constant</i>
  * <details>
    <summary>Classes</summary>

    <details>
    <summary>Tween</summary>
      
    <i>Represents a tween animation.</i>
    * <details>
      <summary>Constructor</summary>
      
      ```python
      Tween(
          instance,
          properties,
          duration,
          tween_type = TweenType.LINEAR
        )
      ```
      + `gif_playback_speed` (str): The GIF playback speed.
      + `instance` (PyGuiInstance): The PyGuiInstance to be tweened.
      + `properties` (Dict[str, Any]): A dictionary of properties to be tweened.
      + `duration` (float): The duration of the tween in seconds.
      + `tween_type` (TweenType): The type of tween to be used.
      </details>
    * <details>
      <summary>Methods</summary>
   
      + `play()`: Starts or resumes the tween.
      + `pause()`: Pauses the tween (Not implemented).
      + `cancel()`: Cancels the tween and resets the PyGuiInstance properties.
      </details>
    * <details>
      <summary>Properties</summary>
   
      + `alpha` (float): Current progress of the tween as a value between 0 and 1.
      </details>
    </details>
    </details>
  * <details>
    <summary>Enums</summary>

    + `TweenStatus`
      + PLAYING: The Tween is currently playing.
      + PAUSED: The Tween is paused.
      + CANCELED: The Tween has been canceled.
      + ENDED: The Tween has ended.
     
    + `TweenType`
      + LINEAR: Linear interpolation.
      + SINE_IN, SINE_OUT, SINE_IN_OUT: Sine easing functions.
      + QUAD_IN, QUAD_OUT, QUAD_IN_OUT: Quadratic easing functions.
      + CUBIC_IN, CUBIC_OUT, CUBIC_IN_OUT: Cubic easing functions.
      + QUART_IN, QUART_OUT, QUART_IN_OUT: Quartic easing functions.
      + QUINT_IN, QUINT_OUT, QUINT_IN_OUT: Quintic easing functions.
      + EXPO_IN, EXPO_OUT, EXPO_IN_OUT: Exponential easing functions.
      + CIRC_IN, CIRC_OUT, CIRC_IN_OUT: Circular easing functions.
      + BACK_IN, BACK_OUT, BACK_IN_OUT: Back easing functions.
      + ELASTIC_IN, ELASTIC_OUT, ELASTIC_IN_OUT: Elastic easing functions.
      + BOUNCE_IN, BOUNCE_OUT, BOUNCE_IN_OUT: Bounce easing functions.
    </details>

  ___

  ![alt text](https://i.imgur.com/KhdNRaS.png)
  
  <i>Service to help facilitate the process of listening for user inputs.</i>
  * <details>
    <summary>Functions</summary>

    + `release_focus(action_name: str, callback: Callable[[Any], Optional[ActionResult]], events: List[int], priority: int = 0, internal: bool = False)`: Binds an action to specific events and assigns a callback function to handle the action.
    + `unbind_action(action_name: str)`: Unbinds an action based on its name.
    </details>
  * <details>
    <summary>Enums</summary>

    + `ActionResult`
      + SINK: The action was handled and should not be passed to other callbacks.
      + PASS: The action was not handled and should be passed to other callbacks.
    </details>
</details>

<details>
  <summary>Utilities</summary>ㅤ<!---Invisible Space--->

  ![alt image](https://i.imgur.com/w1YfgIU.png)

  <i>Represents a signal in PyGui, allowing connections to callback functions.</i>
  * <details>
    <summary>Classes</summary>

    * <details>
      <summary>PyGuiConnection</summary>
      
      <i>Represents a connection between a PyGuiSignal and a callback function.</i>
      * <details>
        <summary>Constructor</summary>
      
        ```python
        PyGuiConnection(signal, callback)
        ```
        + `signal (PyGuiSignal)`: The PyGuiSignal to be connected to.
        + `callback (Callable[[Any], Any])`: The callback function to be connected.
        </details>
      * <details>
        <summary>Methods</summary>
     
        + `disconnect(self)`: Disconnects the connection from the associated PyGuiSignal.
        </details>
      </details>
    * <details>
      <summary>PyGuiSignal</summary>
   
      <i>Represents a signal in PyGui, allowing connections to callback functions.</i>
      * <details>
        <summary>Methods</summary>
        
        + `connect(self, callback: Callable[[Any], Any])` -> `PyGuiConnection`: Connects a callback function to the PyGuiSignal and returns a PyGuiConnection.
        + `fire(self, arguments: Any = None)`: Fires the PyGuiSignal, invoking all connected callback functions.
        + `wait(self)`: Placeholder method for potential future use.
        </details>
      </details>
    </details>

  ___
  
  ![alt image](https://i.imgur.com/p5llAYn.png)

  <i>UDim represents an scaleable (1D and 2D) user interface dimension (UDim) with a scale and offset.</i>
  * <details>
    <summary>Classes</summary>

    * <details>
      <summary>UDim</summary>
      
      <i>Represents a one-dimensional user interface dimension (UDim) with a scale and offset.</i>
      * <details>
        <summary>Constructor</summary>
   
        ```python
        UDim(scale, offset, scale_y, offset_y)
        ```
        + `scale` (float): The scaling factor of the UDim.
        + `offset` (float): The offset of the UDim.
        </details>
      * <details>
        <summary>Properties</summary>
     
        + `scale` (float): The scaling factor of the UDim.
        + `offset` (float): The offset of the UDim.
        </details>
      </details>
    * <details>
      <summary>UDim2</summary>
      
      <i>Represents a two-dimensional user interface dimension (UDim2) with separate X and Y dimensions.</i>
      * <details>
        <summary>Constructor</summary>
   
        ```python
        UDim2(scale_x, offset_x, scale_y, offset_y)
        ```
        + `scale_x` (float): The scaling factor of the X dimension.
        + `offset_x` (float): The offset of the X dimension.
        + `scale_y` (float): The scaling factor of the Y dimension.
        + `offset_y` (float): The offset of the Y dimension.
        </details>
      * <details>
        <summary>Properties</summary>
     
        + `x` (UDim): The UDim instance for the X dimension.
        + `y` (UDim): The UDim instance for the Y dimension.
        </details>
      </details>
    </details>
</details>

![alt text](https://i.imgur.com/jglwtNI.png)

Contributions to pyguilib are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository.
