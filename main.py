import gradio as gr
import colors


def format_result(result):
    if not result:
        return "<p style='color:#999;'>No colours found.</p>"

    html = "<div style='font-family: sans-serif; padding: 8px;'>"
    for colour, count in result:
        r, g, b = colour
        hex_code = f"#{r:02x}{g:02x}{b:02x}"
        html += f"""
        <div style='display:flex; align-items:center; gap:16px; margin-bottom:14px;'>

            <div style='width:64px; height:64px; background:{hex_code}; border-radius:10px; border:1px solid #ddd; flex-shrink:0;'>
            </div>

            <div>
                <div style='font-weight:700; font-size:18px; letter-spacing:1px;'>
                    {hex_code.upper()}
                </div>
                <div style='color:#555; margin:2px 0;'>RGB({r}, {g}, {b})</div>
                <div style='color:#999; font-size:12px;'>{count:,} pixels</div>
            </div>
            
        </div>
        """
    html += "</div>"
    return html


def dominant_colours(image, top_n=1):
    if image is None:
        return "<p style='color:#999;'>Upload an image to see results.</p>"
    img = colors.load_image(image)
    result = colors.dominant_colours(img, top_n=top_n, )
    return format_result(result)


with gr.Blocks(title="Dominant Colour Finder") as demo:
    gr.Markdown("# Dominant Colour Finder. ")
    gr.Markdown("Upload any image to extract its top dominant colours.")

    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(label="Upload an image", type="filepath", height=350, elem_id="image-input")

            top_n_input = gr.Slider(label="Number of colours to show", minimum=1, maximum=10, value=3, step=1, elem_id="top-n-slider")

            button = gr.Button("Find Dominant Colours", variant="primary", size="lg", elem_id="find-colours-btn")

        with gr.Column(scale=1):
            result_output = gr.HTML(label="Dominant Colours", elem_id="result-output")

    button.click(
        fn=dominant_colours,
        inputs=[image_input, top_n_input],
        outputs=result_output,
    )

if __name__ == "__main__":
    demo.launch(share=True, theme=gr.themes.Soft())