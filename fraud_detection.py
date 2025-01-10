
from manim import *

class FraudDetectionScene(Scene):
    def construct(self):
        ############################################################
        # GLOBAL SETTINGS (Minimalistic)
        ############################################################
        self.camera.background_color = BLACK
        TEXT_COLOR = WHITE
        BAR_COLOR = GREY_B            # bars for transaction distribution
        FRAUD_COLOR = GREY            # bar for 'Fraud'
        NON_FRAUD_COLOR = WHITE       # bar for 'Non-Fraud'
        LINE_ACC_COLOR = GREY_B       # line for Accuracy
        LINE_AUC_COLOR = GREY_C       # line for AUC
        AXIS_COLOR = WHITE

        ############################################################
        # 0) TITLE
        ############################################################
        title = Text(
            "Financial Fraud Detection",
            font_size=60, color=TEXT_COLOR
        ).to_edge(UP)
        self.play(FadeIn(title, shift=DOWN))
        self.wait(2)

        ############################################################
        # 1) INTRO DETAILS
        ############################################################
        intro_text = Text(
            "Dataset Size: 6.36M rows, 11 columns
"
            "Total Frauds: 8,213
"
            "No Missing Values",
            font_size=36,
            color=TEXT_COLOR
        )
        intro_text.next_to(title, DOWN, buff=1)
        self.play(Write(intro_text))
        self.wait(3)
        self.play(FadeOut(intro_text))

        ############################################################
        # 2) TRANSACTION TYPES DISTRIBUTION
        ############################################################
        section_1 = Text(
            "1) Transaction Types Distribution",
            font_size=36, color=TEXT_COLOR
        ).to_edge(UP)
        self.play(ReplacementTransform(title, section_1))
        self.wait(1)

        types = ["CASH_OUT", "PAYMENT", "CASH_IN", "TRANSFER", "DEBIT"]
        values = [2237500, 2151495, 1399284, 532909, 41432]
        max_val = max(values)  # 2,237,500
        scale_factor = 5 / max_val

        # We'll spread the bars out more to avoid overlap
        x_axis_1 = NumberLine(
            x_range=[0, len(types)*2, 1],  # e.g. 0..10 if len=5
            length=8,
            color=AXIS_COLOR,
            include_numbers=False
        )
        x_axis_1.shift(DOWN*2)

        bars_1 = VGroup()
        for i, (t, v) in enumerate(zip(types, values)):
            bar_height = v * scale_factor
            bar = Rectangle(
                width=0.6, height=bar_height,
                fill_color=BAR_COLOR, fill_opacity=0.9
            )
            bar.next_to(x_axis_1.n2p(i*2), UP, buff=0)

            label_txt = Text(t, font_size=24, color=TEXT_COLOR)
            label_txt.next_to(bar, DOWN, buff=0.15)

            val_txt = Text(f"{v:,}", font_size=24, color=TEXT_COLOR)
            val_txt.move_to(bar.get_top() + UP*0.3)

            bars_1.add(VGroup(bar, label_txt, val_txt))

        bars_1.shift(UP*0.5)

        self.play(Create(x_axis_1))
        for group in bars_1:
            bar, lbl, val_lbl = group
            self.play(
                GrowFromEdge(bar, DOWN),
                FadeIn(lbl, shift=DOWN),
                FadeIn(val_lbl, shift=UP)
            )
            self.wait(0.2)
        self.wait(1)

        self.play(FadeOut(x_axis_1), FadeOut(bars_1))

        ############################################################
        # 3) FRAUD vs. NON-FRAUD
        ############################################################
        section_2 = Text(
            "2) Fraud vs. Non-Fraud",
            font_size=36, color=TEXT_COLOR
        ).to_edge(UP)
        self.play(ReplacementTransform(section_1, section_2))
        self.wait(1)

        fraud_count = 8213
        non_fraud_count = 6362620 - fraud_count  # 6,354,407
        data_2 = [("Non-Fraud", non_fraud_count), ("Fraud", fraud_count)]
        max_2 = max([val for _, val in data_2])
        scale_2 = 6 / max_2

        x_axis_2 = NumberLine(
            x_range=[0, len(data_2)*2, 1],
            length=6,
            color=AXIS_COLOR,
            include_numbers=False
        )
        x_axis_2.shift(DOWN*2)

        bars_2 = VGroup()
        for i, (lbl, val) in enumerate(data_2):
            bar_height = val * scale_2
            c = NON_FRAUD_COLOR if lbl == "Non-Fraud" else FRAUD_COLOR
            bar = Rectangle(
                width=0.8, height=bar_height,
                fill_color=c, fill_opacity=0.9
            )
            bar.next_to(x_axis_2.n2p(i*2), UP, buff=0)

            lbl_txt = Text(lbl, font_size=24, color=TEXT_COLOR)
            lbl_txt.next_to(bar, DOWN, buff=0.15)

            val_txt = Text(f"{val:,}", font_size=24, color=TEXT_COLOR)
            val_txt.move_to(bar.get_top() + UP*0.3)

            bars_2.add(VGroup(bar, lbl_txt, val_txt))

        bars_2.shift(UP*0.5)

        self.play(Create(x_axis_2))
        for group in bars_2:
            bar, lbl_txt, val_txt = group
            self.play(
                GrowFromEdge(bar, DOWN),
                FadeIn(lbl_txt, shift=DOWN),
                FadeIn(val_txt, shift=UP)
            )
            self.wait(0.2)
        self.wait(1)

        self.play(FadeOut(x_axis_2), FadeOut(bars_2))

        ############################################################
        # 4) TRAINING METRICS (ACCURACY & AUC)
        ############################################################
        section_3 = Text(
            "3) Training Metrics over 8 Epochs",
            font_size=36, color=TEXT_COLOR
        ).to_edge(UP)
        self.play(ReplacementTransform(section_2, section_3))
        self.wait(1)

        epochs = [1,2,3,4,5,6,7,8]
        acc = [0.8066, 0.8535, 0.8547, 0.8718, 0.8614, 0.8612, 0.8479, 0.8654]
        val_acc = [0.8771, 0.8777, 0.8882, 0.8827, 0.8899, 0.8306, 0.8843, 0.8880]
        auc_ = [0.8931, 0.9317, 0.9327, 0.9356, 0.9349, 0.9385, 0.9377, 0.9382]
        val_auc = [0.9348, 0.9390, 0.9385, 0.9417, 0.9415, 0.9416, 0.9417, 0.9421]

        # We'll do side-by-side Axes: left for (acc, val_acc), right for (auc, val_auc)
        left_axes = Axes(
            x_range=[1, 8, 1],
            y_range=[0.80, 0.90, 0.02],
            x_length=5,
            y_length=3,
            axis_config={"stroke_color": AXIS_COLOR},
            tips=False
        ).shift(LEFT*3 + DOWN*1)

        right_axes = Axes(
            x_range=[1, 8, 1],
            y_range=[0.88, 0.95, 0.01],
            x_length=5,
            y_length=3,
            axis_config={"stroke_color": AXIS_COLOR},
            tips=False
        ).shift(RIGHT*3 + DOWN*1)

        # Plot lines on left
        acc_graph = left_axes.plot_line_graph(
            x_values=epochs,
            y_values=acc,
            add_vertex_dots=True,
            line_color=LINE_ACC_COLOR
        )
        val_acc_graph = left_axes.plot_line_graph(
            x_values=epochs,
            y_values=val_acc,
            add_vertex_dots=True,
            line_color=LINE_AUC_COLOR
        )

        # Plot lines on right
        auc_graph = right_axes.plot_line_graph(
            x_values=epochs,
            y_values=auc_,
            add_vertex_dots=True,
            line_color=LINE_ACC_COLOR
        )
        val_auc_graph = right_axes.plot_line_graph(
            x_values=epochs,
            y_values=val_auc,
            add_vertex_dots=True,
            line_color=LINE_AUC_COLOR
        )

        acc_label = Text("Accuracy", font_size=24, color=LINE_ACC_COLOR).next_to(left_axes, UP)
        val_acc_label = Text("Val Accuracy", font_size=24, color=LINE_AUC_COLOR).next_to(left_axes, DOWN)
        auc_label = Text("AUC", font_size=24, color=LINE_ACC_COLOR).next_to(right_axes, UP)
        val_auc_label = Text("Val AUC", font_size=24, color=LINE_AUC_COLOR).next_to(right_axes, DOWN)

        self.play(Create(left_axes), Create(right_axes))
        self.play(Create(acc_graph), Create(val_acc_graph))
        self.play(FadeIn(acc_label), FadeIn(val_acc_label))
        self.play(Create(auc_graph), Create(val_auc_graph))
        self.play(FadeIn(auc_label), FadeIn(val_auc_label))
        self.wait(2)

        self.play(
            *[FadeOut(m) for m in [
                left_axes, right_axes,
                acc_graph, val_acc_graph, auc_graph, val_auc_graph,
                acc_label, val_acc_label, auc_label, val_auc_label
            ]]
        )

        ############################################################
        # 5) CONFUSION MATRIX
        ############################################################
        section_4 = Text(
            "4) Confusion Matrix",
            font_size=36, color=TEXT_COLOR
        ).to_edge(UP)
        self.play(ReplacementTransform(section_3, section_4))
        self.wait(1)

        # approximate matrix values
        matrix_box_size = 1.4
        top_left = Square(matrix_box_size, fill_color=GREY_E, fill_opacity=0.5)
        top_right = Square(matrix_box_size, fill_color=GREY_E, fill_opacity=0.5)
        bottom_left = Square(matrix_box_size, fill_color=GREY_E, fill_opacity=0.5)
        bottom_right = Square(matrix_box_size, fill_color=GREY_E, fill_opacity=0.5)

        top_left.shift(LEFT*1.3 + UP*0.5)
        top_right.next_to(top_left, RIGHT, buff=0)
        bottom_left.next_to(top_left, DOWN, buff=0)
        bottom_right.next_to(bottom_left, RIGHT, buff=0)

        tl_label = Text("TN
1,692,561", font_size=24, color=TEXT_COLOR).move_to(top_left.get_center())
        tr_label = Text("FP
213,761", font_size=24, color=TEXT_COLOR).move_to(top_right.get_center())
        bl_label = Text("FN
394", font_size=24, color=TEXT_COLOR).move_to(bottom_left.get_center())
        br_label = Text("TP
2,070", font_size=24, color=TEXT_COLOR).move_to(bottom_right.get_center())

        actual_label = Text("Actual", font_size=24, color=TEXT_COLOR).move_to(LEFT*3 + UP*0.0)
        predicted_label = Text("Predicted", font_size=24, color=TEXT_COLOR).move_to(UP*2 + RIGHT*0.5)

        actual_nf = Text("Non-Fraud", font_size=20, color=TEXT_COLOR).move_to(top_left.get_left()).shift(LEFT*1.2)
        actual_f = Text("Fraud", font_size=20, color=TEXT_COLOR).move_to(bottom_left.get_left()).shift(LEFT*1.2)
        pred_nf = Text("Non-Fraud", font_size=20, color=TEXT_COLOR).move_to(top_left.get_top()).shift(UP*0.8)
        pred_f = Text("Fraud", font_size=20, color=TEXT_COLOR).move_to(top_right.get_top()).shift(UP*0.8)

        matrix_grp = VGroup(
            top_left, top_right, bottom_left, bottom_right,
            tl_label, tr_label, bl_label, br_label,
            actual_label, predicted_label,
            actual_nf, actual_f, pred_nf, pred_f
        )
        self.play(FadeIn(matrix_grp, shift=UP))
        self.wait(2)
        self.play(FadeOut(matrix_grp))

        ############################################################
        # 6) FINAL METRICS & CONCLUSION
        ############################################################
        section_5 = Text(
            "5) Final Results & Conclusion",
            font_size=36, color=TEXT_COLOR
        ).to_edge(UP)
        self.play(ReplacementTransform(section_4, section_5))
        self.wait(1)

        final_text = Text(
            "Test Loss: 0.2937
"
            "Test Accuracy: 0.8879
"
            "Test AUC: 0.9404
"
            "Recall (Fraud): 0.84
"
            "Weighted Avg F1: ~0.94",
            font_size=28, color=TEXT_COLOR
        )
        final_text.shift(UP*0.5)
        self.play(FadeIn(final_text))
        self.wait(3)

        conclusion = Text(
            "The model effectively detects fraud.
"
            "Next steps: fine-tune or handle imbalance further.
"
            "Thank you!",
            font_size=28, color=TEXT_COLOR
        ).next_to(final_text, DOWN, buff=1)
        self.play(FadeIn(conclusion))
        self.wait(3)

        self.play(FadeOut(final_text), FadeOut(conclusion), FadeOut(section_5))
        self.wait()

        # End Slide
        end_slide = Text("End of Presentation", font_size=36, color=TEXT_COLOR)
        self.play(FadeIn(end_slide, shift=DOWN))
        self.wait(2)
        self.play(FadeOut(end_slide))
        self.wait()
