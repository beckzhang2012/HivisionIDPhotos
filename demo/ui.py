import gradio as gr
import os
import sys
import pathlib

# 添加当前目录和项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from locales import LOCALES
from processor import IDPhotoProcessor

"""
只裁切模式:
1. 如果重新上传了照片，然后点击按钮，第一次会调用不裁切的模式，第二次会调用裁切的模式
"""


def load_description(fp):
    """
    加载title.md文件作为Demo的顶部栏
    """
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def create_ui(
    processor: IDPhotoProcessor,
    root_dir: str,
    human_matting_models: list,
    face_detect_models: list,
    language: list,
):

    # 加载环境变量DEFAULT_LANG, 如果有且在language中，则将DEFAULT_LANG设置为环境变量
    if "DEFAULT_LANG" in os.environ and os.environ["DEFAULT_LANG"] in language:
        DEFAULT_LANG = os.environ["DEFAULT_LANG"]
    else:
        DEFAULT_LANG = language[0]

    DEFAULT_HUMAN_MATTING_MODEL = "modnet_photographic_portrait_matting"
    DEFAULT_FACE_DETECT_MODEL = "retinaface-resnet50"

    if DEFAULT_HUMAN_MATTING_MODEL in human_matting_models:
        human_matting_models.remove(DEFAULT_HUMAN_MATTING_MODEL)
        human_matting_models.insert(0, DEFAULT_HUMAN_MATTING_MODEL)

    if DEFAULT_FACE_DETECT_MODEL not in face_detect_models:
        DEFAULT_FACE_DETECT_MODEL = "mtcnn"

    demo = gr.Blocks(title="HivisionIDPhotos")

    with demo:
        gr.HTML(load_description(os.path.join(root_dir, "demo/assets/title.md")))
        with gr.Row():
            # ------------------------ 左半边 UI ------------------------
            with gr.Column():
                img_input = gr.Image(height=400)

                with gr.Row():
                    # 语言选择器
                    language_options = gr.Dropdown(
                        choices=language,
                        label="Language",
                        value=DEFAULT_LANG,
                    )

                    face_detect_model_options = gr.Dropdown(
                        choices=face_detect_models,
                        label=LOCALES["face_model"][DEFAULT_LANG]["label"],
                        value=DEFAULT_FACE_DETECT_MODEL,
                    )

                    matting_model_options = gr.Dropdown(
                        choices=human_matting_models,
                        label=LOCALES["matting_model"][DEFAULT_LANG]["label"],
                        value=human_matting_models[0],
                    )

                # TAB1 - 关键参数 ------------------------------------------------
                with gr.Tab(
                    LOCALES["key_param"][DEFAULT_LANG]["label"]
                ) as key_parameter_tab:
                    # 尺寸模式
                    with gr.Row():
                        mode_options = gr.Radio(
                            choices=LOCALES["size_mode"][DEFAULT_LANG]["choices"],
                            label=LOCALES["size_mode"][DEFAULT_LANG]["label"],
                            value=LOCALES["size_mode"][DEFAULT_LANG]["choices"][0],
                            min_width=520,
                        )

                    # 尺寸列表
                    with gr.Row(visible=True) as size_list_row:
                        size_list_options = gr.Dropdown(
                            choices=LOCALES["size_list"][DEFAULT_LANG]["choices"],
                            label=LOCALES["size_list"][DEFAULT_LANG]["label"],
                            value=LOCALES["size_list"][DEFAULT_LANG]["choices"][0],
                            elem_id="size_list",
                        )
                    # 自定义尺寸px
                    with gr.Row(visible=False) as custom_size_px:
                        custom_size_height_px = gr.Number(
                            value=413,
                            label=LOCALES["custom_size_px"][DEFAULT_LANG]["height"],
                            interactive=True,
                        )
                        custom_size_width_px = gr.Number(
                            value=295,
                            label=LOCALES["custom_size_px"][DEFAULT_LANG]["width"],
                            interactive=True,
                        )
                    # 自定义尺寸mm
                    with gr.Row(visible=False) as custom_size_mm:
                        custom_size_height_mm = gr.Number(
                            value=35,
                            label=LOCALES["custom_size_mm"][DEFAULT_LANG]["height"],
                            interactive=True,
                        )
                        custom_size_width_mm = gr.Number(
                            value=25,
                            label=LOCALES["custom_size_mm"][DEFAULT_LANG]["width"],
                            interactive=True,
                        )

                    # 背景颜色
                    color_options = gr.Radio(
                        choices=LOCALES["bg_color"][DEFAULT_LANG]["choices"],
                        label=LOCALES["bg_color"][DEFAULT_LANG]["label"],
                        value=LOCALES["bg_color"][DEFAULT_LANG]["choices"][0],
                    )

                    # 自定义颜色RGB
                    with gr.Row(visible=False) as custom_color_rgb:
                        custom_color_R = gr.Number(
                            value=0, label="R", minimum=0, maximum=255, interactive=True
                        )
                        custom_color_G = gr.Number(
                            value=0, label="G", minimum=0, maximum=255, interactive=True
                        )
                        custom_color_B = gr.Number(
                            value=0, label="B", minimum=0, maximum=255, interactive=True
                        )

                    # 自定义颜色HEX
                    with gr.Row(visible=False) as custom_color_hex:
                        custom_color_hex_value = gr.Text(
                            value="000000", label="Hex", interactive=True
                        )

                    # 渲染模式
                    render_options = gr.Radio(
                        choices=LOCALES["render_mode"][DEFAULT_LANG]["choices"],
                        label=LOCALES["render_mode"][DEFAULT_LANG]["label"],
                        value=LOCALES["render_mode"][DEFAULT_LANG]["choices"][0],
                    )

                    with gr.Row():
                        # 插件模式
                        plugin_options = gr.CheckboxGroup(
                            label=LOCALES["plugin"][DEFAULT_LANG]["label"],
                            choices=LOCALES["plugin"][DEFAULT_LANG]["choices"],
                            interactive=True,
                            value=LOCALES["plugin"][DEFAULT_LANG]["value"],
                        )

                # TAB2 - 高级参数 ------------------------------------------------
                with gr.Tab(
                    LOCALES["advance_param"][DEFAULT_LANG]["label"]
                ) as advance_parameter_tab:
                    head_measure_ratio_option = gr.Slider(
                        minimum=0.1,
                        maximum=0.5,
                        value=0.2,
                        step=0.01,
                        label=LOCALES["head_measure_ratio"][DEFAULT_LANG]["label"],
                        interactive=True,
                    )
                    top_distance_option = gr.Slider(
                        minimum=0.02,
                        maximum=0.5,
                        value=0.12,
                        step=0.01,
                        label=LOCALES["top_distance"][DEFAULT_LANG]["label"],
                        interactive=True,
                    )

                    image_kb_options = gr.Radio(
                        choices=LOCALES["image_kb"][DEFAULT_LANG]["choices"],
                        label=LOCALES["image_kb"][DEFAULT_LANG]["label"],
                        value=LOCALES["image_kb"][DEFAULT_LANG]["choices"][0],
                    )

                    custom_image_kb_size = gr.Slider(
                        minimum=10,
                        maximum=1000,
                        value=50,
                        label=LOCALES["image_kb_size"][DEFAULT_LANG]["label"],
                        interactive=True,
                        visible=False,
                    )

                    image_dpi_options = gr.Radio(
                        choices=LOCALES["image_dpi"][DEFAULT_LANG]["choices"],
                        label=LOCALES["image_dpi"][DEFAULT_LANG]["label"],
                        value=LOCALES["image_dpi"][DEFAULT_LANG]["choices"][0],
                    )
                    custom_image_dpi_size = gr.Slider(
                        minimum=72,
                        maximum=600,
                        value=300,
                        label=LOCALES["image_dpi_size"][DEFAULT_LANG]["label"],
                        interactive=True,
                        visible=False,
                    )

                # TAB3 - 美颜 ------------------------------------------------
                with gr.Tab(
                    LOCALES["beauty_tab"][DEFAULT_LANG]["label"]
                ) as beauty_parameter_tab:
                    # 美白组件
                    whitening_option = gr.Slider(
                        label=LOCALES["whitening_strength"][DEFAULT_LANG]["label"],
                        minimum=0,
                        maximum=15,
                        value=2,
                        step=1,
                        interactive=True,
                    )

                    with gr.Row():
                        # 亮度组件
                        brightness_option = gr.Slider(
                            label=LOCALES["brightness_strength"][DEFAULT_LANG]["label"],
                            minimum=-5,
                            maximum=25,
                            value=0,
                            step=1,
                            interactive=True,
                        )
                        # 对比度组件
                        contrast_option = gr.Slider(
                            label=LOCALES["contrast_strength"][DEFAULT_LANG]["label"],
                            minimum=-10,
                            maximum=50,
                            value=0,
                            step=1,
                            interactive=True,
                        )
                        # 饱和度组件
                        saturation_option = gr.Slider(
                            label=LOCALES["saturation_strength"][DEFAULT_LANG]["label"],
                            minimum=-10,
                            maximum=50,
                            value=0,
                            step=1,
                            interactive=True,
                        )

                    # 锐化组件
                    sharpen_option = gr.Slider(
                        label=LOCALES["sharpen_strength"][DEFAULT_LANG]["label"],
                        minimum=0,
                        maximum=5,
                        value=0,
                        step=1,
                        interactive=True,
                    )

                # TAB4 - 水印 ------------------------------------------------
                with gr.Tab(
                    LOCALES["watermark_tab"][DEFAULT_LANG]["label"]
                ) as watermark_parameter_tab:
                    watermark_options = gr.Radio(
                        choices=LOCALES["watermark_switch"][DEFAULT_LANG]["choices"],
                        label=LOCALES["watermark_switch"][DEFAULT_LANG]["label"],
                        value=LOCALES["watermark_switch"][DEFAULT_LANG]["choices"][0],
                    )

                    with gr.Row():
                        watermark_text_options = gr.Text(
                            max_length=20,
                            label=LOCALES["watermark_text"][DEFAULT_LANG]["label"],
                            value=LOCALES["watermark_text"][DEFAULT_LANG]["value"],
                            placeholder=LOCALES["watermark_text"][DEFAULT_LANG][
                                "placeholder"
                            ],
                            interactive=False,
                        )
                        watermark_text_color = gr.ColorPicker(
                            label=LOCALES["watermark_color"][DEFAULT_LANG]["label"],
                            interactive=False,
                            value="#FFFFFF",
                        )

                    watermark_text_size = gr.Slider(
                        minimum=10,
                        maximum=100,
                        value=20,
                        label=LOCALES["watermark_size"][DEFAULT_LANG]["label"],
                        interactive=False,
                        step=1,
                    )

                    watermark_text_opacity = gr.Slider(
                        minimum=0,
                        maximum=1,
                        value=0.15,
                        label=LOCALES["watermark_opacity"][DEFAULT_LANG]["label"],
                        interactive=False,
                        step=0.01,
                    )

                    watermark_text_angle = gr.Slider(
                        minimum=0,
                        maximum=360,
                        value=30,
                        label=LOCALES["watermark_angle"][DEFAULT_LANG]["label"],
                        interactive=False,
                        step=1,
                    )

                    watermark_text_space = gr.Slider(
                        minimum=10,
                        maximum=200,
                        value=25,
                        label=LOCALES["watermark_space"][DEFAULT_LANG]["label"],
                        interactive=False,
                        step=1,
                    )

                    def update_watermark_text_visibility(choice, language):
                        return [
                            gr.update(
                                interactive=(
                                    choice
                                    == LOCALES["watermark_switch"][language]["choices"][
                                        1
                                    ]
                                )
                            )
                        ] * 6

                    watermark_options.change(
                        fn=update_watermark_text_visibility,
                        inputs=[watermark_options, language_options],
                        outputs=[
                            watermark_text_options,
                            watermark_text_color,
                            watermark_text_size,
                            watermark_text_opacity,
                            watermark_text_angle,
                            watermark_text_space,
                        ],
                    )

                # TAB5 - 打印 ------------------------------------------------
                with gr.Tab(
                    LOCALES["print_tab"][DEFAULT_LANG]["label"]
                ) as print_parameter_tab:
                    print_options = gr.Radio(
                        choices=LOCALES["print_switch"][DEFAULT_LANG]["choices"],
                        label=LOCALES["print_switch"][DEFAULT_LANG]["label"],
                        value=LOCALES["print_switch"][DEFAULT_LANG]["choices"][0],
                        interactive=True,
                    )

                # TAB6 - 批量处理 ------------------------------------------------
                with gr.Tab("批量处理") as batch_processing_tab:
                    with gr.Row():
                        # 批量上传组件
                        batch_img_input = gr.Files(
                            label="上传多张照片",
                            file_types=["image"],
                            interactive=True,
                            file_count="multiple",
                        )

                    with gr.Row():
                        # 开始处理按钮
                        batch_process_btn = gr.Button(
                            value="开始批量处理", interactive=True
                        )

                        # 一键下载所有结果按钮
                        batch_download_all_btn = gr.Button(
                            value="一键下载所有结果", interactive=False
                        )

                        # 查看历史记录按钮
                        batch_view_history_btn = gr.Button(
                            value="查看历史记录", interactive=True
                        )

                    # 进度显示组件
                    batch_progress = gr.Progress()

                    # 任务状态表格
                    batch_task_table = gr.Dataframe(
                        headers=["文件名", "状态", "失败原因", "操作"],
                        datatype=["str", "str", "str", "str"],
                        interactive=False,
                        height=300,
                    )

                    # 结果展示组件
                    batch_result_gallery = gr.Gallery(
                        label="处理结果", height=400, format="png", columns=4
                    )

                    # 历史记录展示组件
                    batch_history_gallery = gr.Gallery(
                        label="历史记录", height=400, format="png", columns=4
                    )

                img_but = gr.Button(
                    LOCALES["button"][DEFAULT_LANG]["label"],
                    elem_id="btn",
                    variant="primary",
                )

                example_images = gr.Examples(
                    inputs=[img_input],
                    examples=[
                        [path.as_posix()]
                        for path in sorted(
                            pathlib.Path(os.path.join(root_dir, "demo/images")).rglob(
                                "*.jpg"
                            )
                        )
                    ],
                )

            # ---------------- 右半边 UI ----------------
            with gr.Column():
                notification = gr.Text(
                    label=LOCALES["notification"][DEFAULT_LANG]["label"], visible=False
                )
                with gr.Row():
                    # 标准照
                    img_output_standard = gr.Image(
                        label=LOCALES["standard_photo"][DEFAULT_LANG]["label"],
                        height=350,
                        format="png",
                    )
                    # 高清照
                    img_output_standard_hd = gr.Image(
                        label=LOCALES["hd_photo"][DEFAULT_LANG]["label"],
                        height=350,
                        format="png",
                    )
                # 排版照
                img_output_layout = gr.Image(
                    label=LOCALES["layout_photo"][DEFAULT_LANG]["label"],
                    height=350,
                    format="png",
                )
                # 模版照片
                with gr.Accordion(
                    LOCALES["template_photo"][DEFAULT_LANG]["label"], open=False
                ) as template_image_accordion:
                    img_output_template = gr.Gallery(
                        label=LOCALES["template_photo"][DEFAULT_LANG]["label"],
                        height=350,
                        format="png",
                    )
                # 抠图图像
                with gr.Accordion(
                    LOCALES["matting_image"][DEFAULT_LANG]["label"], open=False
                ) as matting_image_accordion:
                    with gr.Row():
                        img_output_standard_png = gr.Image(
                            label=LOCALES["standard_photo_png"][DEFAULT_LANG]["label"],
                            height=350,
                            format="png",
                            elem_id="standard_photo_png",
                        )
                        img_output_standard_hd_png = gr.Image(
                            label=LOCALES["hd_photo_png"][DEFAULT_LANG]["label"],
                            height=350,
                            format="png",
                            elem_id="hd_photo_png",
                        )

            # ---------------- 多语言切换函数 ----------------
            def change_language(language):
                return {
                    face_detect_model_options: gr.update(
                        label=LOCALES["face_model"][language]["label"]
                    ),
                    matting_model_options: gr.update(
                        label=LOCALES["matting_model"][language]["label"]
                    ),
                    size_list_options: gr.update(
                        label=LOCALES["size_list"][language]["label"],
                        choices=LOCALES["size_list"][language]["choices"],
                        value=LOCALES["size_list"][language]["choices"][0],
                    ),
                    mode_options: gr.update(
                        label=LOCALES["size_mode"][language]["label"],
                        choices=LOCALES["size_mode"][language]["choices"],
                        value=LOCALES["size_mode"][language]["choices"][0],
                    ),
                    color_options: gr.update(
                        label=LOCALES["bg_color"][language]["label"],
                        choices=LOCALES["bg_color"][language]["choices"],
                        value=LOCALES["bg_color"][language]["choices"][0],
                    ),
                    img_but: gr.update(value=LOCALES["button"][language]["label"]),
                    render_options: gr.update(
                        label=LOCALES["render_mode"][language]["label"],
                        choices=LOCALES["render_mode"][language]["choices"],
                        value=LOCALES["render_mode"][language]["choices"][0],
                    ),
                    image_kb_options: gr.update(
                        label=LOCALES["image_kb_size"][language]["label"],
                        choices=LOCALES["image_kb"][language]["choices"],
                        value=LOCALES["image_kb"][language]["choices"][0],
                    ),
                    custom_image_kb_size: gr.update(
                        label=LOCALES["image_kb"][language]["label"]
                    ),
                    notification: gr.update(
                        label=LOCALES["notification"][language]["label"]
                    ),
                    img_output_standard: gr.update(
                        label=LOCALES["standard_photo"][language]["label"]
                    ),
                    img_output_standard_hd: gr.update(
                        label=LOCALES["hd_photo"][language]["label"]
                    ),
                    img_output_standard_png: gr.update(
                        label=LOCALES["standard_photo_png"][language]["label"]
                    ),
                    img_output_standard_hd_png: gr.update(
                        label=LOCALES["hd_photo_png"][language]["label"]
                    ),
                    img_output_layout: gr.update(
                        label=LOCALES["layout_photo"][language]["label"]
                    ),
                    head_measure_ratio_option: gr.update(
                        label=LOCALES["head_measure_ratio"][language]["label"]
                    ),
                    top_distance_option: gr.update(
                        label=LOCALES["top_distance"][language]["label"]
                    ),
                    key_parameter_tab: gr.update(
                        label=LOCALES["key_param"][language]["label"]
                    ),
                    advance_parameter_tab: gr.update(
                        label=LOCALES["advance_param"][language]["label"]
                    ),
                    watermark_parameter_tab: gr.update(
                        label=LOCALES["watermark_tab"][language]["label"]
                    ),
                    watermark_text_options: gr.update(
                        label=LOCALES["watermark_text"][language]["label"],
                        placeholder=LOCALES["watermark_text"][language]["placeholder"],
                    ),
                    watermark_text_color: gr.update(
                        label=LOCALES["watermark_color"][language]["label"]
                    ),
                    watermark_text_size: gr.update(
                        label=LOCALES["watermark_size"][language]["label"]
                    ),
                    watermark_text_opacity: gr.update(
                        label=LOCALES["watermark_opacity"][language]["label"]
                    ),
                    watermark_text_angle: gr.update(
                        label=LOCALES["watermark_angle"][language]["label"]
                    ),
                    watermark_text_space: gr.update(
                        label=LOCALES["watermark_space"][language]["label"]
                    ),
                    watermark_options: gr.update(
                        label=LOCALES["watermark_switch"][language]["label"],
                        choices=LOCALES["watermark_switch"][language]["choices"],
                        value=LOCALES["watermark_switch"][language]["choices"][0],
                    ),
                    matting_image_accordion: gr.update(
                        label=LOCALES["matting_image"][language]["label"]
                    ),
                    beauty_parameter_tab: gr.update(
                        label=LOCALES["beauty_tab"][language]["label"]
                    ),
                    whitening_option: gr.update(
                        label=LOCALES["whitening_strength"][language]["label"]
                    ),
                    image_dpi_options: gr.update(
                        label=LOCALES["image_dpi"][language]["label"],
                        choices=LOCALES["image_dpi"][language]["choices"],
                        value=LOCALES["image_dpi"][language]["choices"][0],
                    ),
                    custom_image_dpi_size: gr.update(
                        label=LOCALES["image_dpi"][language]["label"]
                    ),
                    brightness_option: gr.update(
                        label=LOCALES["brightness_strength"][language]["label"]
                    ),
                    contrast_option: gr.update(
                        label=LOCALES["contrast_strength"][language]["label"]
                    ),
                    sharpen_option: gr.update(
                        label=LOCALES["sharpen_strength"][language]["label"]
                    ),
                    saturation_option: gr.update(
                        label=LOCALES["saturation_strength"][language]["label"]
                    ),
                    custom_size_width_px: gr.update(
                        label=LOCALES["custom_size_px"][language]["width"]
                    ),
                    custom_size_height_px: gr.update(
                        label=LOCALES["custom_size_px"][language]["height"]
                    ),
                    custom_size_width_mm: gr.update(
                        label=LOCALES["custom_size_mm"][language]["width"]
                    ),
                    custom_size_height_mm: gr.update(
                        label=LOCALES["custom_size_mm"][language]["height"]
                    ),
                    img_output_template: gr.update(
                        label=LOCALES["template_photo"][language]["label"]
                    ),
                    template_image_accordion: gr.update(
                        label=LOCALES["template_photo"][language]["label"]
                    ),
                    plugin_options: gr.update(
                        label=LOCALES["plugin"][language]["label"],
                        choices=LOCALES["plugin"][language]["choices"],
                        value=LOCALES["plugin"][language]["choices"][0],
                    ),
                    print_parameter_tab: gr.update(
                        label=LOCALES["print_tab"][language]["label"]
                    ),
                    print_options: gr.update(
                        label=LOCALES["print_switch"][language]["label"],
                        choices=LOCALES["print_switch"][language]["choices"],
                        value=LOCALES["print_switch"][language]["choices"][0],
                    ),
                }

            def change_visibility(option, lang, locales_key, custom_component):
                return {
                    custom_component: gr.update(
                        visible=option == LOCALES[locales_key][lang]["choices"][-1]
                    )
                }

            def change_color(colors, lang):
                return {
                    custom_color_rgb: gr.update(
                        visible=colors == LOCALES["bg_color"][lang]["choices"][-2]
                    ),
                    custom_color_hex: gr.update(
                        visible=colors == LOCALES["bg_color"][lang]["choices"][-1]
                    ),
                }

            def change_size_mode(size_option_item, lang):
                choices = LOCALES["size_mode"][lang]["choices"]
                # 如果选择自定义尺寸mm
                if size_option_item == choices[3]:
                    return {
                        custom_size_px: gr.update(visible=False),
                        custom_size_mm: gr.update(visible=True),
                        size_list_row: gr.update(visible=False),
                        plugin_options: gr.update(interactive=True),
                    }
                # 如果选择自定义尺寸px
                elif size_option_item == choices[2]:
                    return {
                        custom_size_px: gr.update(visible=True),
                        custom_size_mm: gr.update(visible=False),
                        size_list_row: gr.update(visible=False),
                        plugin_options: gr.update(interactive=True),
                    }
                # 如果选择只换底，则隐藏所有尺寸组件
                elif size_option_item == choices[1]:
                    return {
                        custom_size_px: gr.update(visible=False),
                        custom_size_mm: gr.update(visible=False),
                        size_list_row: gr.update(visible=False),
                        plugin_options: gr.update(interactive=False),
                    }
                # 如果选择预设尺寸，则隐藏自定义尺寸组件
                else:
                    return {
                        custom_size_px: gr.update(visible=False),
                        custom_size_mm: gr.update(visible=False),
                        size_list_row: gr.update(visible=True),
                        plugin_options: gr.update(interactive=True),
                    }

            def change_image_kb(image_kb_option, lang):
                return change_visibility(
                    image_kb_option, lang, "image_kb", custom_image_kb_size
                )

            def change_image_dpi(image_dpi_option, lang):
                return change_visibility(
                    image_dpi_option, lang, "image_dpi", custom_image_dpi_size
                )

            # ---------------- 绑定事件 ----------------
            # 语言切换
            language_options.input(
                change_language,
                inputs=[language_options],
                outputs=[
                    size_list_options,
                    mode_options,
                    color_options,
                    img_but,
                    render_options,
                    image_kb_options,
                    matting_model_options,
                    face_detect_model_options,
                    custom_image_kb_size,
                    notification,
                    img_output_standard,
                    img_output_standard_hd,
                    img_output_standard_png,
                    img_output_standard_hd_png,
                    img_output_layout,
                    head_measure_ratio_option,
                    top_distance_option,
                    key_parameter_tab,
                    advance_parameter_tab,
                    watermark_parameter_tab,
                    watermark_text_options,
                    watermark_text_color,
                    watermark_text_size,
                    watermark_text_opacity,
                    watermark_text_angle,
                    watermark_text_space,
                    watermark_options,
                    matting_image_accordion,
                    beauty_parameter_tab,
                    whitening_option,
                    image_dpi_options,
                    custom_image_dpi_size,
                    brightness_option,
                    contrast_option,
                    sharpen_option,
                    saturation_option,
                    plugin_options,
                    custom_size_width_px,
                    custom_size_height_px,
                    custom_size_width_mm,
                    custom_size_height_mm,
                    img_output_template,
                    template_image_accordion,
                    print_parameter_tab,
                    print_options,
                ],
            )

            # ---------------- 设置隐藏/显示交互效果 ----------------
            # 尺寸模式
            mode_options.input(
                change_size_mode,
                inputs=[mode_options, language_options],
                outputs=[
                    custom_size_px,
                    custom_size_mm,
                    size_list_row,
                    plugin_options,
                ],
            )

            # 颜色
            color_options.input(
                change_color,
                inputs=[color_options, language_options],
                outputs=[custom_color_rgb, custom_color_hex],
            )

            # 图片kb
            image_kb_options.input(
                change_image_kb,
                inputs=[image_kb_options, language_options],
                outputs=[custom_image_kb_size],
            )

            # 图片dpi
            image_dpi_options.input(
                change_image_dpi,
                inputs=[image_dpi_options, language_options],
                outputs=[custom_image_dpi_size],
            )

            # ---------------- 批量处理逻辑 ----------------
            import json
            import os
            import time
            from PIL import Image
            import io

            # 任务状态存储
            batch_tasks = []
            # 处理结果存储
            batch_results = []
            # 历史记录文件路径
            history_file = os.path.join(root_dir, "batch_processing_history.json")

            # 加载历史记录
            def load_history():
                if os.path.exists(history_file):
                    with open(history_file, "r", encoding="utf-8") as f:
                        return json.load(f)
                return []

            # 保存历史记录
            def save_history(history):
                with open(history_file, "w", encoding="utf-8") as f:
                    json.dump(history, f, ensure_ascii=False, indent=4)

            # 更新任务状态表格
            def update_task_table():
                return [task[:3] for task in batch_tasks]

            # 批量处理函数
            def batch_process(files, progress=gr.Progress()):
                if not files:
                    return gr.update(visible=True, value="请先上传照片")

                # 重置任务列表和结果列表
                batch_tasks.clear()
                batch_results.clear()

                # 初始化任务列表
                for file in files:
                    batch_tasks.append([os.path.basename(file.name), "等待", "", ""])

                # 更新任务状态表格
                gr.update(batch_task_table, value=update_task_table())

                total_files = len(files)

                for i, file in enumerate(files):
                    # 更新任务状态为处理中
                    batch_tasks[i][1] = "处理中"
                    gr.update(batch_task_table, value=update_task_table())

                    progress(
                        i / total_files, desc=f"正在处理第 {i+1}/{total_files} 张照片"
                    )

                    try:
                        # 读取图片
                        image = gr.load_image(file.name)

                        # 调用现有的处理函数
                        result = processor.process(
                            input_image=image,
                            mode_option=mode_options.value,
                            size_list_option=size_list_options.value,
                            color_option=color_options.value,
                            render_option=render_options.value,
                            image_kb_options=image_kb_options.value,
                            custom_color_R=custom_color_R.value,
                            custom_color_G=custom_color_G.value,
                            custom_color_B=custom_color_B.value,
                            custom_color_hex_value=custom_color_hex_value.value,
                            custom_size_height=custom_size_height_px.value,
                            custom_size_width=custom_size_width_px.value,
                            custom_size_height_mm=custom_size_height_mm.value,
                            custom_size_width_mm=custom_size_width_mm.value,
                            custom_image_kb=custom_image_kb_size.value,
                            language=language_options.value,
                            matting_model_option=matting_model_options.value,
                            watermark_option=watermark_options.value,
                            watermark_text=watermark_text_options.value,
                            watermark_text_color=watermark_text_color.value,
                            watermark_text_size=watermark_text_size.value,
                            watermark_text_opacity=watermark_text_opacity.value,
                            watermark_text_angle=watermark_text_angle.value,
                            watermark_text_space=watermark_text_space.value,
                            face_detect_option=face_detect_model_options.value,
                            head_measure_ratio=head_measure_ratio_option.value,
                            top_distance_max=top_distance_option.value,
                            whitening_strength=whitening_option.value,
                            image_dpi_option=image_dpi_options.value,
                            custom_image_dpi=custom_image_dpi_size.value,
                            brightness_strength=brightness_option.value,
                            contrast_strength=contrast_option.value,
                            sharpen_strength=sharpen_option.value,
                            saturation_strength=saturation_option.value,
                            plugin_option=plugin_options.value,
                            print_switch=print_options.value,
                        )

                        # 处理成功
                        batch_tasks[i][1] = "完成"
                        batch_tasks[i][3] = "下载"

                        # 保存处理结果
                        if result[0] is not None:
                            batch_results.append(
                                (result[0], f"{os.path.basename(file.name)} - 处理结果")
                            )

                    except Exception as e:
                        # 处理失败
                        batch_tasks[i][1] = "失败"
                        batch_tasks[i][2] = str(e)
                        batch_tasks[i][3] = "重试"

                    # 更新任务状态表格
                    gr.update(batch_task_table, value=update_task_table())

                # 保存到历史记录
                history = load_history()
                history.append(
                    {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "tasks": batch_tasks.copy(),
                        "results": batch_results.copy(),
                    }
                )
                save_history(history)

                # 启用一键下载按钮
                gr.update(batch_download_all_btn, interactive=True)

                return batch_results

            # 重试处理函数
            def retry_process(file_name):
                # 找到对应的任务
                for i, task in enumerate(batch_tasks):
                    if task[0] == file_name and task[1] == "失败":
                        # 更新任务状态为处理中
                        batch_tasks[i][1] = "处理中"
                        batch_tasks[i][2] = ""
                        gr.update(batch_task_table, value=update_task_table())

                        try:
                            # 重新读取图片
                            for file in batch_img_input.value:
                                if os.path.basename(file.name) == file_name:
                                    image = gr.load_image(file.name)
                                    break

                            # 调用现有的处理函数
                            result = processor.process(
                                input_image=image,
                                mode_option=mode_options.value,
                                size_list_option=size_list_options.value,
                                color_option=color_options.value,
                                render_option=render_options.value,
                                image_kb_options=image_kb_options.value,
                                custom_color_R=custom_color_R.value,
                                custom_color_G=custom_color_G.value,
                                custom_color_B=custom_color_B.value,
                                custom_color_hex_value=custom_color_hex_value.value,
                                custom_size_height=custom_size_height_px.value,
                                custom_size_width=custom_size_width_px.value,
                                custom_size_height_mm=custom_size_height_mm.value,
                                custom_size_width_mm=custom_size_width_mm.value,
                                custom_image_kb=custom_image_kb_size.value,
                                language=language_options.value,
                                matting_model_option=matting_model_options.value,
                                watermark_option=watermark_options.value,
                                watermark_text=watermark_text_options.value,
                                watermark_text_color=watermark_text_color.value,
                                watermark_text_size=watermark_text_size.value,
                                watermark_text_opacity=watermark_text_opacity.value,
                                watermark_text_angle=watermark_text_angle.value,
                                watermark_text_space=watermark_text_space.value,
                                face_detect_option=face_detect_model_options.value,
                                head_measure_ratio=head_measure_ratio_option.value,
                                top_distance_max=top_distance_option.value,
                                whitening_strength=whitening_option.value,
                                image_dpi_option=image_dpi_options.value,
                                custom_image_dpi=custom_image_dpi_size.value,
                                brightness_strength=brightness_option.value,
                                contrast_strength=contrast_option.value,
                                sharpen_strength=sharpen_option.value,
                                saturation_strength=saturation_option.value,
                                plugin_option=plugin_options.value,
                                print_switch=print_options.value,
                            )

                            # 处理成功
                            batch_tasks[i][1] = "完成"
                            batch_tasks[i][3] = "下载"

                            # 更新结果列表
                            if result[0] is not None:
                                batch_results[i] = (
                                    result[0],
                                    f"{file_name} - 处理结果",
                                )

                        except Exception as e:
                            # 处理失败
                            batch_tasks[i][1] = "失败"
                            batch_tasks[i][2] = str(e)
                            batch_tasks[i][3] = "重试"

                        # 更新任务状态表格和结果画廊
                        gr.update(batch_task_table, value=update_task_table())
                        gr.update(batch_result_gallery, value=batch_results)

                        break

                return gr.update()

            # 一键下载所有结果函数
            def download_all_results():
                if not batch_results:
                    return gr.update(visible=True, value="暂无处理结果")

                # 创建临时目录保存所有结果
                temp_dir = os.path.join(root_dir, "temp_batch_results")
                os.makedirs(temp_dir, exist_ok=True)

                # 保存所有结果图片
                for i, (img, title) in enumerate(batch_results):
                    img_path = os.path.join(temp_dir, f"result_{i+1}.jpg")
                    img.save(img_path)

                # 创建压缩文件
                import zipfile

                zip_path = os.path.join(root_dir, "batch_results.zip")
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            zipf.write(os.path.join(root, file), file)

                # 清理临时目录
                import shutil

                shutil.rmtree(temp_dir)

                return gr.update(visible=True, value="所有结果已打包下载")

            # 查看历史记录函数
            def view_history():
                history = load_history()
                if not history:
                    return gr.update(visible=True, value="暂无历史记录")

                # 获取最新的历史记录
                latest_history = history[-1]

                # 显示历史记录结果
                return latest_history["results"]

            # 绑定批量处理按钮事件
            batch_process_btn.click(
                batch_process, inputs=[batch_img_input], outputs=[batch_result_gallery]
            )

            # 绑定一键下载按钮事件
            batch_download_all_btn.click(
                download_all_results, inputs=[], outputs=[batch_notification]
            )

            # 重试按钮点击事件处理
            def on_retry_click(file_name):
                retry_process(file_name)
                return gr.update()

            # 绑定重试按钮事件
            batch_task_table.click(
                on_retry_click,
                inputs=[batch_task_table.selected_rows],
                outputs=[batch_task_table],
            )

            # 查看历史记录函数
            def view_history():
                history = load_history()
                if not history:
                    return gr.update(visible=True, value="暂无历史记录")

                # 获取最新的历史记录
                latest_history = history[-1]

                # 显示历史记录结果
                return latest_history["results"]

            # 绑定查看历史记录按钮事件
            batch_view_history_btn.click(
                view_history, inputs=[], outputs=[batch_history_gallery]
            )

            img_but.click(
                processor.process,
                inputs=[
                    img_input,
                    mode_options,
                    size_list_options,
                    color_options,
                    render_options,
                    image_kb_options,
                    custom_color_R,
                    custom_color_G,
                    custom_color_B,
                    custom_color_hex_value,
                    custom_size_height_px,
                    custom_size_width_px,
                    custom_size_height_mm,
                    custom_size_width_mm,
                    custom_image_kb_size,
                    language_options,
                    matting_model_options,
                    watermark_options,
                    watermark_text_options,
                    watermark_text_color,
                    watermark_text_size,
                    watermark_text_opacity,
                    watermark_text_angle,
                    watermark_text_space,
                    face_detect_model_options,
                    head_measure_ratio_option,
                    top_distance_option,
                    whitening_option,
                    image_dpi_options,
                    custom_image_dpi_size,
                    brightness_option,
                    contrast_option,
                    sharpen_option,
                    saturation_option,
                    plugin_options,
                    print_options,
                ],
                outputs=[
                    img_output_standard,
                    img_output_standard_hd,
                    img_output_standard_png,
                    img_output_standard_hd_png,
                    img_output_layout,
                    img_output_template,
                    template_image_accordion,
                    notification,
                ],
            )

    return demo
