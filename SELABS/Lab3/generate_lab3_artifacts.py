"""
PES University | Department of Computer Science & Engineering
Software Engineering Lab (UE24CS252AA) — Lab 3: Component Modelling & Architectural Pattern Selection
System: Self-Service Coffee Kiosk System

Generates all Lab 3 deliverables:
1. Architecture_Diagram.png & Architecture_Diagram.pdf (UML Component Diagram)
2. Architecture_Diagram.drawio (Diagrams.net XML)
3. Architecture_Justification_Document.docx (1-Page Word Document)
4. Architecture_Justification_Document.pdf (1-Page PDF Document)
5. Architecture_Specification.pdf (Full Specification PDF)
6. Architecture_Specification.md (Markdown Technical Document)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def draw_uml_component(ax, x, y, width, height, name, stereotype="<<component>>", subtext=None, fillcolor="#FFFFFF", bordercolor="#334155", accent_color="#3B82F6"):
    # Drop shadow
    shadow = patches.FancyBboxPatch(
        (x + 0.5, y - 0.5), width, height,
        boxstyle="round,pad=0.2,rounding_size=1.5",
        linewidth=0, facecolor="#CBD5E1", zorder=2
    )
    ax.add_patch(shadow)

    # Component body
    rect = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.2,rounding_size=1.5",
        linewidth=1.8, edgecolor=bordercolor, facecolor=fillcolor, zorder=3
    )
    ax.add_patch(rect)
    
    # Top header bar
    hdr_bar = patches.FancyBboxPatch(
        (x + 0.2, y + height - 2.8), width - 0.4, 2.6,
        boxstyle="round,pad=0.1,rounding_size=0.8",
        linewidth=0, facecolor=accent_color, zorder=4
    )
    ax.add_patch(hdr_bar)
    
    # Standard UML 2 Component Icon in upper-right corner
    icon_w = 4.2
    icon_h = 3.2
    icon_x = x + width - icon_w - 2.2
    icon_y = y + height - icon_h - 4.0
    icon_rect = patches.Rectangle((icon_x, icon_y), icon_w, icon_h, linewidth=1.1, edgecolor=bordercolor, facecolor="#FFFFFF", zorder=5)
    ax.add_patch(icon_rect)
    # two protruding tabs on left of icon
    tab_w = 1.6
    tab_h = 0.9
    t1 = patches.Rectangle((icon_x - 0.8, icon_y + icon_h - 1.2), tab_w, tab_h, linewidth=0.9, edgecolor=bordercolor, facecolor="#E2E8F0", zorder=6)
    t2 = patches.Rectangle((icon_x - 0.8, icon_y + 0.3), tab_w, tab_h, linewidth=0.9, edgecolor=bordercolor, facecolor="#E2E8F0", zorder=6)
    ax.add_patch(t1)
    ax.add_patch(t2)
    
    # Centered text
    center_x = x + width / 2.0
    ax.text(center_x, y + height - 5.5, stereotype, ha='center', va='center', fontsize=8.5, fontstyle='italic', color='#64748B', weight='medium', zorder=7)
    ax.text(center_x, y + height / 2.0 - 0.5, name, ha='center', va='center', fontsize=11, weight='bold', color='#0F172A', zorder=7)
    if subtext:
        ax.text(center_x, y + 2.8, subtext, ha='center', va='center', fontsize=7.2, color='#475569', zorder=7)

def generate_diagram(output_png, output_pdf):
    fig, ax = plt.subplots(figsize=(15, 11), dpi=300)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 120)
    ax.axis('off')
    
    bg = patches.Rectangle((0, 0), 160, 120, facecolor="#F8FAFC", zorder=0)
    ax.add_patch(bg)
    
    # Title Banner
    title_rect = patches.FancyBboxPatch((8, 107), 144, 9.5, boxstyle="round,pad=0.5,rounding_size=2",
                                        facecolor="#1E293B", edgecolor="#0F172A", linewidth=1.5, zorder=2)
    ax.add_patch(title_rect)
    ax.text(80, 113.0, "Self-Service Coffee Kiosk System — UML Component Diagram",
            ha='center', va='center', fontsize=14.5, weight='bold', color='#FFFFFF', zorder=3)
    ax.text(80, 109.0, "Layered Architectural Pattern | PES University Software Engineering Lab 3 (UE24CS252AA)",
            ha='center', va='center', fontsize=8.5, color='#94A3B8', zorder=3)

    # 1. Presentation Layer Box
    layer1_box = patches.FancyBboxPatch((10, 83), 140, 21, boxstyle="round,pad=0.8,rounding_size=3",
                                        facecolor="#EFF6FF", edgecolor="#3B82F6", linewidth=1.8, zorder=1)
    ax.add_patch(layer1_box)
    l1_tab = patches.FancyBboxPatch((14, 99.5), 32, 4.2, boxstyle="round,pad=0.2,rounding_size=1",
                                    facecolor="#3B82F6", edgecolor="#2563EB", linewidth=1, zorder=2)
    ax.add_patch(l1_tab)
    ax.text(30, 101.6, "Presentation Layer", ha='center', va='center', fontsize=9, weight='bold', color='#FFFFFF', zorder=3)
    
    # Component: User Interface Component
    draw_uml_component(ax, 50, 85.5, 60, 15.5, "User Interface Component",
                       subtext="Touch Screen Interaction  |  Menu Selection  |  Size & Type Select",
                       fillcolor="#FFFFFF", bordercolor="#2563EB", accent_color="#3B82F6")

    # 2. Business Layer Box
    layer2_box = patches.FancyBboxPatch((10, 34), 140, 44, boxstyle="round,pad=0.8,rounding_size=3",
                                        facecolor="#F0FDF4", edgecolor="#16A34A", linewidth=1.8, zorder=1)
    ax.add_patch(layer2_box)
    l2_tab = patches.FancyBboxPatch((14, 73.5), 28, 4.2, boxstyle="round,pad=0.2,rounding_size=1",
                                    facecolor="#16A34A", edgecolor="#15803D", linewidth=1, zorder=2)
    ax.add_patch(l2_tab)
    ax.text(28, 75.6, "Business Layer", ha='center', va='center', fontsize=9, weight='bold', color='#FFFFFF', zorder=3)
    
    # Component: Order Manager Component (Top Center of Business Layer)
    draw_uml_component(ax, 50, 58, 60, 15, "Order Manager Component",
                       subtext="Order Lifecycle Orchestration  |  Price Calculation  |  Transaction Coordination",
                       fillcolor="#FFFFFF", bordercolor="#16A34A", accent_color="#16A34A")

    # Component: Payment Service Component (Bottom Left of Business Layer)
    draw_uml_component(ax, 14, 37, 54, 14.5, "Payment Service Component",
                       subtext="EMV Card Terminal Bridge  |  PCI Tokenization  |  Credit Card Only",
                       fillcolor="#FFFFFF", bordercolor="#16A34A", accent_color="#059669")

    # Component: Receipt Printer Component (Bottom Right of Business Layer)
    draw_uml_component(ax, 92, 37, 54, 14.5, "Receipt Printer Component",
                       subtext="ESC/POS Driver  |  Itemized Slip Formatter  |  Hardware Status",
                       fillcolor="#FFFFFF", bordercolor="#16A34A", accent_color="#059669")

    # 3. Data Layer Box
    layer3_box = patches.FancyBboxPatch((10, 8), 140, 22, boxstyle="round,pad=0.8,rounding_size=3",
                                        facecolor="#FFFBEB", edgecolor="#D97706", linewidth=1.8, zorder=1)
    ax.add_patch(layer3_box)
    l3_tab = patches.FancyBboxPatch((14, 25.5), 24, 4.2, boxstyle="round,pad=0.2,rounding_size=1",
                                    facecolor="#D97706", edgecolor="#B45309", linewidth=1, zorder=2)
    ax.add_patch(l3_tab)
    ax.text(26, 27.6, "Data Layer", ha='center', va='center', fontsize=9, weight='bold', color='#FFFFFF', zorder=3)
    
    # Component: Database Component
    draw_uml_component(ax, 50, 10.5, 60, 14.5, "Database Component",
                       subtext="Menu & Pricing Catalog  |  Order Transaction Store  |  Local SQLite DB",
                       fillcolor="#FFFFFF", bordercolor="#D97706", accent_color="#D97706")

    # ================= INTERFACES (UML BALL & SOCKET NOTATION) =================
    
    # --- Interface 1: Order Interface (Between User Interface & Order Manager) ---
    mid_y1 = 79.2
    ax.plot([80, 80], [85.5, mid_y1 + 1.2], color="#0284C7", linewidth=2.2, zorder=7)
    socket1 = patches.Arc((80, mid_y1 + 0.2), 3.8, 3.8, angle=0, theta1=0, theta2=180,
                          color="#0284C7", linewidth=2.5, zorder=8)
    ax.add_patch(socket1)
    ax.plot([80, 80], [73.0, mid_y1 - 0.7], color="#0284C7", linewidth=2.2, zorder=7)
    ball1 = patches.Circle((80, mid_y1 - 0.1), 1.0, facecolor="#0284C7", edgecolor="#0369A1", linewidth=1.2, zorder=9)
    ax.add_patch(ball1)
    
    ax.text(83.5, mid_y1 + 1.2, "«interface» Order Interface", fontsize=8.8, weight='bold', color='#0369A1', va='center', zorder=10)
    ax.text(83.5, mid_y1 - 1.2, "selectCoffee(type, size), calculateTotal(), submitOrder()", fontsize=7.2, color='#475569', va='center', zorder=10)

    # --- Interface 2: Payment Interface (Order Manager to Payment Service) ---
    ax.plot([50, 41, 41], [62, 62, 55.6], color="#059669", linewidth=2.0, zorder=7)
    socket2 = patches.Arc((41, 54.8), 3.6, 3.6, angle=0, theta1=0, theta2=180,
                          color="#059669", linewidth=2.4, zorder=8)
    ax.add_patch(socket2)
    ax.plot([41, 41], [51.5, 53.7], color="#059669", linewidth=2.0, zorder=7)
    ball2 = patches.Circle((41, 54.4), 1.0, facecolor="#059669", edgecolor="#047857", linewidth=1.2, zorder=9)
    ax.add_patch(ball2)
    
    ax.text(38, 57.0, "«interface» Payment Interface", fontsize=8.2, weight='bold', color='#047857', ha='right', va='center', zorder=10)
    ax.text(38, 54.8, "processPayment(), authorizeCard() [PCI SDK]", fontsize=7.0, color='#475569', ha='right', va='center', zorder=10)

    # --- Interface 3: Receipt Interface (Order Manager to Receipt Printer) ---
    ax.plot([110, 119, 119], [62, 62, 55.6], color="#059669", linewidth=2.0, zorder=7)
    socket3 = patches.Arc((119, 54.8), 3.6, 3.6, angle=0, theta1=0, theta2=180,
                          color="#059669", linewidth=2.4, zorder=8)
    ax.add_patch(socket3)
    ax.plot([119, 119], [51.5, 53.7], color="#059669", linewidth=2.0, zorder=7)
    ball3 = patches.Circle((119, 54.4), 1.0, facecolor="#059669", edgecolor="#047857", linewidth=1.2, zorder=9)
    ax.add_patch(ball3)
    
    ax.text(122, 57.0, "«interface» Receipt Interface", fontsize=8.2, weight='bold', color='#047857', ha='left', va='center', zorder=10)
    ax.text(122, 54.8, "printReceipt(), getPrinterStatus() [ESC/POS]", fontsize=7.0, color='#475569', ha='left', va='center', zorder=10)

    # --- Interface 4: Database Interface (Order Manager to Database Component) ---
    mid_y4 = 30.5
    ax.plot([80, 80], [58, mid_y4 + 1.2], color="#D97706", linewidth=2.2, zorder=7)
    socket4 = patches.Arc((80, mid_y4 + 0.2), 3.8, 3.8, angle=0, theta1=0, theta2=180,
                          color="#D97706", linewidth=2.5, zorder=8)
    ax.add_patch(socket4)
    ax.plot([80, 80], [25.0, mid_y4 - 0.7], color="#D97706", linewidth=2.2, zorder=7)
    ball4 = patches.Circle((80, mid_y4 - 0.1), 1.0, facecolor="#D97706", edgecolor="#B45309", linewidth=1.2, zorder=9)
    ax.add_patch(ball4)
    
    ax.text(83.5, mid_y4 + 1.2, "«interface» Database Interface", fontsize=8.8, weight='bold', color='#B45309', va='center', zorder=10)
    ax.text(83.5, mid_y4 - 1.2, "getMenuData(), getPricing(), saveOrderRecord() [SQL / JDBC]", fontsize=7.2, color='#475569', va='center', zorder=10)

    # --- Legend & System Scope Footer ---
    legend_box = patches.FancyBboxPatch((10, 1.5), 140, 5, boxstyle="round,pad=0.2,rounding_size=1.2",
                                        facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1, zorder=2)
    ax.add_patch(legend_box)
    
    ax.plot([13, 15], [4.0, 4.0], color="#334155", linewidth=1.5, zorder=3)
    b_leg = patches.Circle((16, 4.0), 0.9, facecolor="#334155", edgecolor="#0F172A", zorder=4)
    ax.add_patch(b_leg)
    ax.text(18, 4.0, "Provided Interface (Ball)", fontsize=7.5, va='center', color="#334155", weight='bold', zorder=4)
    
    ax.plot([46, 48], [4.0, 4.0], color="#334155", linewidth=1.5, zorder=3)
    s_leg = patches.Arc((49, 4.0), 2.8, 2.8, angle=0, theta1=90, theta2=270, color="#334155", linewidth=1.8, zorder=4)
    ax.add_patch(s_leg)
    ax.text(51.5, 4.0, "Required Interface (Socket)", fontsize=7.5, va='center', color="#334155", weight='bold', zorder=4)
    
    ax.text(82, 4.0, "Coffee Types: Espresso, Americano, Latte | Sizes: Small, Large | Payment: Credit Card | Hardware: Receipt Printer, Touch Screen",
            fontsize=7.0, fontstyle='italic', va='center', color="#475569", zorder=4)

    plt.tight_layout()
    plt.savefig(output_png, format='png', dpi=300, bbox_inches='tight')
    plt.savefig(output_pdf, format='pdf', bbox_inches='tight')
    plt.close()
    print(f"Generated {output_png} and {output_pdf}")

def generate_drawio_xml(output_drawio):
    xml_content = """<mxfile host="Electron" modified="2026-10-02T18:50:00.000Z" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="coffee-kiosk-layered-architecture" name="Lab 3 - Coffee Kiosk Architecture">
    <mxGraphModel dx="1280" dy="840" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#f8fafc" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <mxCell id="hdr" value="&lt;b&gt;Self-Service Coffee Kiosk System — UML Component Diagram&lt;/b&gt;&lt;br/&gt;&lt;font style=&quot;font-size: 11px; color: #cbd5e1;&quot;&gt;Layered Architectural Pattern | PES University Software Engineering Lab 3 (UE24CS252AA)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1e293b;strokeColor=#0f172a;fontColor=#ffffff;fontSize=15;arcSize=10;" vertex="1" parent="1">
          <mxGeometry x="60" y="20" width="1040" height="50" as="geometry" />
        </mxCell>

        <mxCell id="layer_pres" value="&lt;b&gt;Presentation Layer&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;fontColor=#1e40af;fontSize=13;startSize=26;rounded=1;arcSize=6;collapsible=0;" vertex="1" parent="1">
          <mxGeometry x="60" y="90" width="1040" height="150" as="geometry" />
        </mxCell>

        <mxCell id="comp_ui" value="«component»&lt;br/&gt;&lt;b&gt;User Interface Component&lt;/b&gt;&lt;br/&gt;&lt;font style=&quot;font-size: 10px; color: #475569;&quot;&gt;• Touch Screen Interaction Handler&lt;br/&gt;• Menu Display (Espresso, Americano, Latte)&lt;br/&gt;• Drink Size Selection (Small, Large)&lt;br/&gt;• Payment &amp;amp; Receipt Status Rendering&lt;/font&gt;" style="html=1;dropTarget=0;whiteSpace=wrap;rounded=1;arcSize=8;fillColor=#ffffff;strokeColor=#2563eb;strokeWidth=1.5;fontSize=12;fontColor=#0f172a;" vertex="1" parent="layer_pres">
          <mxGeometry x="360" y="38" width="320" height="95" as="geometry" />
        </mxCell>
        <mxCell id="comp_ui_icon" value="" style="shape=module;jettyWidth=8;jettyHeight=4;fillColor=#ffffff;strokeColor=#2563eb;" vertex="1" parent="comp_ui">
          <mxGeometry x="1" width="20" height="20" relative="1" as="geometry">
            <mxPoint x="-26" y="6" as="offset" />
          </mxGeometry>
        </mxCell>

        <mxCell id="layer_bus" value="&lt;b&gt;Business Layer&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor=#f0fdf4;strokeColor=#16a34a;fontColor=#166534;fontSize=13;startSize=26;rounded=1;arcSize=6;collapsible=0;" vertex="1" parent="1">
          <mxGeometry x="60" y="270" width="1040" height="340" as="geometry" />
        </mxCell>

        <mxCell id="comp_order" value="«component»&lt;br/&gt;&lt;b&gt;Order Manager Component&lt;/b&gt;&lt;br/&gt;&lt;font style=&quot;font-size: 10px; color: #475569;&quot;&gt;• Coordinates Order Lifecycle &amp;amp; Workflow&lt;br/&gt;• Calculates Pricing by Coffee Type &amp;amp; Size&lt;br/&gt;• Triggers Card Authorization via Payment Service&lt;br/&gt;• Dispatches Itemized Job to Receipt Printer&lt;/font&gt;" style="html=1;dropTarget=0;whiteSpace=wrap;rounded=1;arcSize=8;fillColor=#ffffff;strokeColor=#16a34a;strokeWidth=1.5;fontSize=12;fontColor=#0f172a;" vertex="1" parent="layer_bus">
          <mxGeometry x="360" y="45" width="320" height="100" as="geometry" />
        </mxCell>
        <mxCell id="comp_order_icon" value="" style="shape=module;jettyWidth=8;jettyHeight=4;fillColor=#ffffff;strokeColor=#16a34a;" vertex="1" parent="comp_order">
          <mxGeometry x="1" width="20" height="20" relative="1" as="geometry">
            <mxPoint x="-26" y="6" as="offset" />
          </mxGeometry>
        </mxCell>

        <mxCell id="comp_pay" value="«component»&lt;br/&gt;&lt;b&gt;Payment Service Component&lt;/b&gt;&lt;br/&gt;&lt;font style=&quot;font-size: 10px; color: #475569;&quot;&gt;• Card Processing Hardware Bridge (EMV)&lt;br/&gt;• Encrypted Transaction Gateway Integration&lt;br/&gt;• PCI-DSS Tokenization &amp;amp; Authorization&lt;br/&gt;• Enforces Credit Card Only Policy&lt;/font&gt;" style="html=1;dropTarget=0;whiteSpace=wrap;rounded=1;arcSize=8;fillColor=#ffffff;strokeColor=#16a34a;strokeWidth=1.5;fontSize=12;fontColor=#0f172a;" vertex="1" parent="layer_bus">
          <mxGeometry x="60" y="210" width="310" height="95" as="geometry" />
        </mxCell>
        <mxCell id="comp_pay_icon" value="" style="shape=module;jettyWidth=8;jettyHeight=4;fillColor=#ffffff;strokeColor=#16a34a;" vertex="1" parent="comp_pay">
          <mxGeometry x="1" width="20" height="20" relative="1" as="geometry">
            <mxPoint x="-26" y="6" as="offset" />
          </mxGeometry>
        </mxCell>

        <mxCell id="comp_print" value="«component»&lt;br/&gt;&lt;b&gt;Receipt Printer Component&lt;/b&gt;&lt;br/&gt;&lt;font style=&quot;font-size: 10px; color: #475569;&quot;&gt;• Direct Hardware Driver Connection (USB/Serial)&lt;br/&gt;• Formats Itemized Order &amp;amp; Transaction Slip&lt;br/&gt;• ESC/POS Thermal Print Commands&lt;br/&gt;• Hardware Health &amp;amp; Paper Status Monitoring&lt;/font&gt;" style="html=1;dropTarget=0;whiteSpace=wrap;rounded=1;arcSize=8;fillColor=#ffffff;strokeColor=#16a34a;strokeWidth=1.5;fontSize=12;fontColor=#0f172a;" vertex="1" parent="layer_bus">
          <mxGeometry x="670" y="210" width="310" height="95" as="geometry" />
        </mxCell>
        <mxCell id="comp_print_icon" value="" style="shape=module;jettyWidth=8;jettyHeight=4;fillColor=#ffffff;strokeColor=#16a34a;" vertex="1" parent="comp_print">
          <mxGeometry x="1" width="20" height="20" relative="1" as="geometry">
            <mxPoint x="-26" y="6" as="offset" />
          </mxGeometry>
        </mxCell>

        <mxCell id="layer_data" value="&lt;b&gt;Data Layer&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor=#fffbeb;strokeColor=#d97706;fontColor=#92400e;fontSize=13;startSize=26;rounded=1;arcSize=6;collapsible=0;" vertex="1" parent="1">
          <mxGeometry x="60" y="640" width="1040" height="150" as="geometry" />
        </mxCell>

        <mxCell id="comp_db" value="«component»&lt;br/&gt;&lt;b&gt;Database Component&lt;/b&gt;&lt;br/&gt;&lt;font style=&quot;font-size: 10px; color: #475569;&quot;&gt;• Embedded Relational Database (SQLite / Local JDBC)&lt;br/&gt;• Menu Data Store (Espresso, Americano, Latte)&lt;br/&gt;• Pricing &amp;amp; Tax Matrix (Small, Large Tiering)&lt;br/&gt;• Persistent Transaction Log &amp;amp; Audit History&lt;/font&gt;" style="html=1;dropTarget=0;whiteSpace=wrap;rounded=1;arcSize=8;fillColor=#ffffff;strokeColor=#d97706;strokeWidth=1.5;fontSize=12;fontColor=#0f172a;" vertex="1" parent="layer_data">
          <mxGeometry x="360" y="38" width="320" height="95" as="geometry" />
        </mxCell>
        <mxCell id="comp_db_icon" value="" style="shape=module;jettyWidth=8;jettyHeight=4;fillColor=#ffffff;strokeColor=#d97706;" vertex="1" parent="comp_db">
          <mxGeometry x="1" width="20" height="20" relative="1" as="geometry">
            <mxPoint x="-26" y="6" as="offset" />
          </mxGeometry>
        </mxCell>

        <!-- Interfaces (Ball and Socket) -->
        <mxCell id="if_order_ball" value="" style="shape=ellipse;whiteSpace=wrap;html=1;fillColor=#0284c7;strokeColor=#0369a1;aspect=fixed;" vertex="1" parent="1">
          <mxGeometry x="572" y="254" width="16" height="16" as="geometry" />
        </mxCell>
        <mxCell id="conn_order_prov" value="" style="endArrow=none;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;strokeColor=#0284c7;strokeWidth=2;" edge="1" parent="1" source="if_order_ball" target="comp_order">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn_order_req" value="&lt;b&gt;Order Interface&lt;/b&gt;&lt;br/&gt;selectCoffee(), getStatus()" style="endArrow=oval;endFill=0;html=1;rounded=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;strokeColor=#0284c7;strokeWidth=2;fontSize=10;fontColor=#0369a1;labelPosition=right;verticalLabelPosition=middle;align=left;" edge="1" parent="1" source="comp_ui" target="if_order_ball">
          <mxGeometry x="0.2" y="10" relative="1" as="geometry" />
        </mxCell>

        <mxCell id="if_pay_ball" value="" style="shape=ellipse;whiteSpace=wrap;html=1;fillColor=#059669;strokeColor=#047857;aspect=fixed;" vertex="1" parent="1">
          <mxGeometry x="267" y="445" width="16" height="16" as="geometry" />
        </mxCell>
        <mxCell id="conn_pay_prov" value="" style="endArrow=none;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;strokeColor=#059669;strokeWidth=2;" edge="1" parent="1" source="if_pay_ball" target="comp_pay">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn_pay_req" value="&lt;b&gt;Payment Interface&lt;/b&gt;&lt;br/&gt;processPayment(), authorize()" style="endArrow=oval;endFill=0;html=1;rounded=0;exitX=0.2;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;strokeColor=#059669;strokeWidth=2;fontSize=10;fontColor=#047857;labelPosition=left;verticalLabelPosition=middle;align=right;" edge="1" parent="1" source="comp_order" target="if_pay_ball">
          <mxGeometry x="-0.2" y="-10" relative="1" as="geometry" />
        </mxCell>

        <mxCell id="if_print_ball" value="" style="shape=ellipse;whiteSpace=wrap;html=1;fillColor=#059669;strokeColor=#047857;aspect=fixed;" vertex="1" parent="1">
          <mxGeometry x="877" y="445" width="16" height="16" as="geometry" />
        </mxCell>
        <mxCell id="conn_print_prov" value="" style="endArrow=none;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;strokeColor=#059669;strokeWidth=2;" edge="1" parent="1" source="if_print_ball" target="comp_print">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn_print_req" value="&lt;b&gt;Receipt Interface&lt;/b&gt;&lt;br/&gt;printReceipt(), getStatus()" style="endArrow=oval;endFill=0;html=1;rounded=0;exitX=0.8;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;strokeColor=#059669;strokeWidth=2;fontSize=10;fontColor=#047857;labelPosition=right;verticalLabelPosition=middle;align=left;" edge="1" parent="1" source="comp_order" target="if_print_ball">
          <mxGeometry x="0.2" y="-10" relative="1" as="geometry" />
        </mxCell>

        <mxCell id="if_db_ball" value="" style="shape=ellipse;whiteSpace=wrap;html=1;fillColor=#d97706;strokeColor=#b45309;aspect=fixed;" vertex="1" parent="1">
          <mxGeometry x="572" y="625" width="16" height="16" as="geometry" />
        </mxCell>
        <mxCell id="conn_db_prov" value="" style="endArrow=none;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;strokeColor=#d97706;strokeWidth=2;" edge="1" parent="1" source="if_db_ball" target="comp_db">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn_db_req" value="&lt;b&gt;Database Interface&lt;/b&gt;&lt;br/&gt;getMenu(), getPricing(), logOrder()" style="endArrow=oval;endFill=0;html=1;rounded=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;strokeColor=#d97706;strokeWidth=2;fontSize=10;fontColor=#b45309;labelPosition=right;verticalLabelPosition=middle;align=left;" edge="1" parent="1" source="comp_order" target="if_db_ball">
          <mxGeometry x="0.2" y="10" relative="1" as="geometry" />
        </mxCell>

        <mxCell id="leg" value="&lt;b&gt;UML Notation Legend:&lt;/b&gt; &amp;nbsp; &amp;nbsp; ◯ Provided Interface (Ball / Facet) &amp;nbsp; &amp;nbsp; ◖ Required Interface (Socket / Receptacle) &amp;nbsp; &amp;nbsp; ─── Assembly Connector &amp;nbsp; &amp;nbsp; | &amp;nbsp; &amp;nbsp; &lt;b&gt;Hardware &amp;amp; Scope:&lt;/b&gt; Touch Screen, Receipt Printer Hardware, Credit Card Terminal, 3 Coffee Types, 2 Drink Sizes" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#94a3b8;fontColor=#334155;fontSize=10;align=center;" vertex="1" parent="1">
          <mxGeometry x="60" y="805" width="1040" height="30" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    with open(output_drawio, 'w', encoding='utf-8') as f:
        f.write(xml_content.strip())
    print(f"Generated {output_drawio}")

def generate_word_justification(output_docx):
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.55)
        section.bottom_margin = Inches(0.55)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)
        
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.12
    normal_style.paragraph_format.space_after = Pt(3.5)

    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_header.paragraph_format.space_after = Pt(2)
    run_inst = p_header.add_run("PES UNIVERSITY | DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\n")
    run_inst.font.size = Pt(8.5)
    run_inst.font.bold = True
    run_inst.font.color.rgb = RGBColor(100, 116, 139)
    
    run_title = p_header.add_run("Lab 3: Component Modelling & Architectural Pattern Selection\n")
    run_title.font.size = Pt(13)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42)
    
    run_sub = p_header.add_run("Software Engineering Lab (UE24CS252AA) — Architectural Justification Document")
    run_sub.font.size = Pt(9)
    run_sub.font.color.rgb = RGBColor(71, 85, 105)

    table_meta = doc.add_table(rows=1, cols=4)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_meta.autofit = False
    col_widths = [Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.8)]
    meta_data = [
        ("Student Name:", "Sujay Hegde"),
        ("SRN:", "PES1UG24CS478"),
        ("Assigned System:", "Coffee Kiosk System"),
        ("Architectural Style:", "Layered Architecture")
    ]
    hdr_cells = table_meta.rows[0].cells
    for i, (label, val) in enumerate(meta_data):
        hdr_cells[i].width = col_widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        r1 = p.add_run(f"{label} ")
        r1.bold = True
        r1.font.size = Pt(8)
        r1.font.color.rgb = RGBColor(15, 23, 42)
        r2 = p.add_run(val)
        r2.font.size = Pt(8)
        r2.font.color.rgb = RGBColor(2, 132, 199)
        shading = parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w')))
        hdr_cells[i]._tc.get_or_add_tcPr().append(shading)

    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    p_sel = doc.add_paragraph()
    p_sel.paragraph_format.space_after = Pt(5)
    p_sel.paragraph_format.space_before = Pt(2)
    run_banner = p_sel.add_run('Architecture Selection: "We chose Layered Architecture for the Self-Service Coffee Kiosk System."')
    run_banner.bold = True
    run_banner.font.size = Pt(10.5)
    run_banner.font.color.rgb = RGBColor(30, 58, 138)

    # 1. Architectural Choice
    p_choice = doc.add_paragraph()
    r_ch_title = p_choice.add_run("1. Architectural Choice: ")
    r_ch_title.bold = True
    r_ch_title.font.color.rgb = RGBColor(15, 23, 42)
    p_choice.add_run(
        "We selected the classic 3-Tier Layered Architecture consisting of a Presentation Layer (Touch Screen User Interface Component), "
        "a Business Layer (Order Manager, Payment Service, and Receipt Printer Components), and a Data Layer (Database Component). "
        "Each layer encapsulates discrete responsibilities with strict top-down dependency flow, allowing components to interact solely through well-defined UML provided and required interfaces."
    )

    # 2. Two Reasons
    p_reasons = doc.add_paragraph()
    r_r_title = p_reasons.add_run("2. Two Reasons for Architectural Choice (Scenario-Related):\n")
    r_r_title.bold = True
    r_r_title.font.color.rgb = RGBColor(15, 23, 42)
    
    r_r1 = p_reasons.add_run("• Reason 1 — Modularity & Hardware Decoupling in a Standalone Embedded Kiosk: ")
    r_r1.bold = True
    p_reasons.add_run(
        "The kiosk interacts with specialized peripheral hardware (capacitive touch screen, EMV credit card reader terminal, and thermal receipt printer). "
        "A Layered style isolates these physical device interactions within modular business/hardware components. For example, if the receipt printer model or touch screen OS changes, only the respective driver component needs modification while core order orchestration and database schemas remain unaffected.\n"
    )
    
    r_r2 = p_reasons.add_run("• Reason 2 — Elimination of Unnecessary Distributed Complexity: ")
    r_r2.bold = True
    p_reasons.add_run(
        "Unlike web-scale distributed e-commerce apps, a café coffee kiosk runs as a localized single-station embedded terminal serving sequential in-person orders. "
        "Adopting a Microservices architecture would introduce severe networking latency, serialization overhead, and multi-service failure states at checkout. Layered architecture guarantees near-instant in-process IPC method invocation, deterministic execution order, and trivial deployment on dedicated kiosk hardware."
    )

    # 3. Security Advantage
    p_sec = doc.add_paragraph()
    r_sec_title = p_sec.add_run("3. Security Advantage:\n")
    r_sec_title.bold = True
    r_sec_title.font.color.rgb = RGBColor(15, 23, 42)
    p_sec.add_run(
        "Strict Layer Isolation & PCI-DSS Cardholder Protection: Because customers can pay exclusively via credit card, isolating payment logic inside an encapsulated Payment Service Component protects sensitive payment flows. "
        "The Presentation Layer (touch screen) has zero direct visibility or direct database access to stored transactional records or credit card memory buffers. "
        "All card transactions are funneled through the Payment Interface, which handles point-to-point encryption and tokenization with the card reader hardware before notifying the Order Manager, minimizing PCI compliance scope and preventing memory-scraping attacks on the public kiosk."
    )

    # 4. Performance Benefit
    p_perf = doc.add_paragraph()
    r_perf_title = p_perf.add_run("4. Performance Benefit:\n")
    r_perf_title.bold = True
    r_perf_title.font.color.rgb = RGBColor(15, 23, 42)
    p_perf.add_run(
        "Zero-Network Overhead & Local In-Memory Query Optimization: In a busy café rush, low latency is critical to prevent customer queues. "
        "In this Layered design, components reside in the same runtime host and interact through ultra-fast, local compiled/IPC interfaces rather than REST/gRPC HTTP network round-trips. "
        "Furthermore, static menu data (Espresso, Americano, Latte) and size pricing (Small, Large) are pre-loaded from the Database Component into fast local memory caches upon system boot, enabling instantaneous touch-screen rendering (<10ms) and swift end-to-end checkout completion."
    )

    p_tbl_lbl = doc.add_paragraph()
    p_tbl_lbl.paragraph_format.space_before = Pt(3)
    p_tbl_lbl.paragraph_format.space_after = Pt(2)
    r_tbl_title = p_tbl_lbl.add_run("Summary of System Components (5) & Required/Provided Interfaces (4):")
    r_tbl_title.bold = True
    r_tbl_title.font.size = Pt(8.5)
    r_tbl_title.font.color.rgb = RGBColor(15, 23, 42)

    table = doc.add_table(rows=6, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    t_widths = [Inches(1.8), Inches(1.3), Inches(1.9), Inches(2.2)]
    headers = ["Component Name", "Assigned Layer", "Interfaces (Ball / Socket)", "Functional Responsibility"]
    
    row_hdr = table.rows[0]
    for j, h_text in enumerate(headers):
        cell = row_hdr.cells[j]
        cell.width = t_widths[j]
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        run = p.add_run(h_text)
        run.bold = True
        run.font.size = Pt(7.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        shading = parse_xml(r'<w:shd {} w:fill="1E293B"/>'.format(nsdecls('w')))
        cell._tc.get_or_add_tcPr().append(shading)

    table_rows = [
        ("User Interface Component", "Presentation", "Requires: Order Interface (Socket)", "Touch screen display, drink & size selection, status rendering"),
        ("Order Manager Component", "Business", "Provides: Order Interface (Ball)\nRequires: Payment, Receipt, DB (Sockets)", "Central orchestrator; computes prices; coordinates pay & print"),
        ("Payment Service Component", "Business", "Provides: Payment Interface (Ball)", "Card terminal hardware bridge, PCI encryption, card-only billing"),
        ("Receipt Printer Component", "Business (HW)", "Provides: Receipt Interface (Ball)", "ESC/POS driver interface, formats receipt slip, paper checks"),
        ("Database Component", "Data Layer", "Provides: Database Interface (Ball)", "Menu store (Espresso, Americano, Latte), pricing & order logs")
    ]

    for idx, (c_name, c_layer, c_if, c_resp) in enumerate(table_rows):
        row = table.rows[idx + 1]
        fill_hex = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        for j, val in enumerate([c_name, c_layer, c_if, c_resp]):
            cell = row.cells[j]
            cell.width = t_widths[j]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(val)
            run.font.size = Pt(7.2)
            if j == 0:
                run.bold = True
            shading = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), fill_hex))
            cell._tc.get_or_add_tcPr().append(shading)

    doc.save(output_docx)
    print(f"Generated {output_docx}")

def generate_pdf_justification(output_pdf):
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=14,
        textColor=colors.HexColor('#0F172A'), alignment=1
    )
    inst_style = ParagraphStyle(
        'InstTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=9,
        textColor=colors.HexColor('#64748B'), alignment=1
    )
    sub_style = ParagraphStyle(
        'SubTitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=10,
        textColor=colors.HexColor('#475569'), alignment=1
    )
    banner_style = ParagraphStyle(
        'BannerStyle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=12,
        textColor=colors.HexColor('#1E3A8A'), spaceBefore=3, spaceAfter=4
    )
    body_style = ParagraphStyle(
        'BodyDark', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.2, leading=10.2,
        textColor=colors.HexColor('#1E293B'), spaceAfter=3.5
    )
    bold_prefix = ParagraphStyle(
        'BoldPrefix', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=10.5,
        textColor=colors.HexColor('#0F172A'), spaceBefore=2, spaceAfter=1
    )
    table_text = ParagraphStyle(
        'TableText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=6.8, leading=8.2,
        textColor=colors.HexColor('#1E293B')
    )
    table_hdr = ParagraphStyle(
        'TableHdr', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7, leading=8.5,
        textColor=colors.white
    )

    story = []
    story.append(Paragraph("PES UNIVERSITY | DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", inst_style))
    story.append(Paragraph("Lab 3: Component Modelling & Architectural Pattern Selection", title_style))
    story.append(Paragraph("Software Engineering Lab (UE24CS252AA) — Architectural Justification Document", sub_style))
    story.append(Spacer(1, 4))
    
    meta_table_data = [
        [
            Paragraph("<b>Student:</b> Sujay Hegde", table_text),
            Paragraph("<b>SRN:</b> PES1UG24CS478", table_text),
            Paragraph("<b>Assigned System:</b> Coffee Kiosk", table_text),
            Paragraph("<b>Style:</b> Layered Architecture", table_text)
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[135, 135, 135, 135])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>Architecture Selection:</b> "We chose Layered Architecture for the Self-Service Coffee Kiosk System."', banner_style))
    
    story.append(Paragraph("1. Architectural Choice:", bold_prefix))
    story.append(Paragraph(
        "We selected the classic 3-Tier Layered Architecture consisting of a Presentation Layer (Touch Screen User Interface Component), "
        "a Business Layer (Order Manager, Payment Service, and Receipt Printer Components), and a Data Layer (Database Component). "
        "Each layer encapsulates discrete responsibilities with strict top-down dependency flow, allowing components to interact solely through well-defined UML provided and required interfaces.",
        body_style
    ))
    
    story.append(Paragraph("2. Two Reasons for Architectural Choice (Scenario-Related):", bold_prefix))
    story.append(Paragraph(
        "• <b>Reason 1 — Modularity & Hardware Decoupling in an Embedded Kiosk:</b> "
        "The kiosk interacts with specialized peripheral hardware (capacitive touch screen, EMV credit card reader terminal, and thermal receipt printer). "
        "A Layered style isolates these physical device interactions within modular business/hardware components. For example, if the receipt printer model or touch screen OS changes, only the respective driver component needs modification while core order orchestration and database schemas remain unaffected.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Reason 2 — Elimination of Unnecessary Distributed Complexity:</b> "
        "Unlike web-scale distributed e-commerce apps, a café coffee kiosk runs as a localized single-station embedded terminal serving sequential in-person orders. "
        "Adopting a Microservices architecture would introduce severe networking latency, serialization overhead, and multi-service failure states at checkout. Layered architecture guarantees near-instant in-process IPC method invocation, deterministic execution order, and trivial deployment on dedicated kiosk hardware.",
        body_style
    ))
    
    story.append(Paragraph("3. Security Advantage:", bold_prefix))
    story.append(Paragraph(
        "<b>Strict Layer Isolation & PCI-DSS Cardholder Protection:</b> Because customers can pay exclusively via credit card, isolating payment logic inside an encapsulated Payment Service Component protects sensitive payment flows. "
        "The Presentation Layer (touch screen) has zero direct visibility or direct database access to stored transactional records or credit card memory buffers. "
        "All card transactions are funneled through the Payment Interface, which handles point-to-point encryption and tokenization with the card reader hardware before notifying the Order Manager, minimizing PCI compliance scope and preventing memory-scraping attacks on the public kiosk.",
        body_style
    ))
    
    story.append(Paragraph("4. Performance Benefit:", bold_prefix))
    story.append(Paragraph(
        "<b>Zero-Network Overhead & Local In-Memory Query Optimization:</b> In a busy café rush, low latency is critical to prevent customer queues. "
        "In this Layered design, components reside in the same runtime host and interact through ultra-fast, local compiled/IPC interfaces rather than REST/gRPC HTTP network round-trips. "
        "Furthermore, static menu data (Espresso, Americano, Latte) and size pricing (Small, Large) are pre-loaded from the Database Component into fast local memory caches upon system boot, enabling instantaneous touch-screen rendering (&lt;10ms) and swift end-to-end checkout completion.",
        body_style
    ))
    
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Summary of System Components (5) & Required/Provided Interfaces (4):</b>", bold_prefix))
    
    tbl_data = [
        [Paragraph("Component Name", table_hdr), Paragraph("Assigned Layer", table_hdr), Paragraph("Interfaces (Ball / Socket)", table_hdr), Paragraph("Functional Responsibility", table_hdr)],
        [Paragraph("<b>User Interface</b>", table_text), Paragraph("Presentation", table_text), Paragraph("Requires: Order Interface (Socket)", table_text), Paragraph("Touch screen display, drink & size selection, status rendering", table_text)],
        [Paragraph("<b>Order Manager</b>", table_text), Paragraph("Business", table_text), Paragraph("Provides: Order Interface (Ball)<br/>Requires: Payment, Receipt, DB (Sockets)", table_text), Paragraph("Central orchestrator; computes prices; coordinates pay & print", table_text)],
        [Paragraph("<b>Payment Service</b>", table_text), Paragraph("Business", table_text), Paragraph("Provides: Payment Interface (Ball)", table_text), Paragraph("Card terminal hardware bridge, PCI encryption, card-only billing", table_text)],
        [Paragraph("<b>Receipt Printer</b>", table_text), Paragraph("Business (HW)", table_text), Paragraph("Provides: Receipt Interface (Ball)", table_text), Paragraph("ESC/POS driver interface, formats receipt slip, paper checks", table_text)],
        [Paragraph("<b>Database</b>", table_text), Paragraph("Data Layer", table_text), Paragraph("Provides: Database Interface (Ball)", table_text), Paragraph("Menu store (Espresso, Americano, Latte), pricing & order logs", table_text)]
    ]
    t_summary = Table(tbl_data, colWidths=[120, 85, 155, 180])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F8FAFC')),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#F8FAFC')),
        ('BACKGROUND', (0,4), (-1,4), colors.white),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_summary)
    
    doc.build(story)
    print(f"Generated {output_pdf}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_png = os.path.join(base_dir, "Architecture_Diagram.png")
    output_pdf_diag = os.path.join(base_dir, "Architecture_Diagram.pdf")
    output_drawio = os.path.join(base_dir, "Architecture_Diagram.drawio")
    output_docx = os.path.join(base_dir, "Architecture_Justification_Document.docx")
    output_pdf_just = os.path.join(base_dir, "Architecture_Justification_Document.pdf")
    
    print("Generating Lab 3 Deliverables...")
    generate_diagram(output_png, output_pdf_diag)
    generate_drawio_xml(output_drawio)
    generate_word_justification(output_docx)
    generate_pdf_justification(output_pdf_just)
    print("All Lab 3 deliverables successfully generated!")
