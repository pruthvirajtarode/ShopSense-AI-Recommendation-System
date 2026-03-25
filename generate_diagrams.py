import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_system_architecture_diagram():
    """Create System Architecture Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Define positions
    positions = {
        'user': (6, 9),
        'streamlit': (6, 7),
        'fastapi': (6, 5),
        'ml': (6, 3),
        'data': (6, 1)
    }

    # Draw boxes
    boxes = [
        ('Users\n(Browser/Client)', positions['user'], '#FF6B6B'),
        ('Streamlit Frontend\n(UI, Charts, Reports)', positions['streamlit'], '#4ECDC4'),
        ('FastAPI Backend\n(Recommendation API)', positions['fastapi'], '#45B7D1'),
        ('ML Layer (ALS)\n(Model Loading, Prediction)', positions['ml'], '#96CEB4'),
        ('Data Storage\n(products.csv, interactions)', positions['data'], '#FFEAA7')
    ]

    for text, pos, color in boxes:
        rect = FancyBboxPatch((pos[0]-2, pos[1]-0.5), 4, 1, boxstyle="round,pad=0.1",
                             facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(pos[0], pos[1], text, ha='center', va='center', fontsize=10, fontweight='bold')

    # Draw arrows
    for i in range(len(boxes)-1):
        start_pos = boxes[i][1]
        end_pos = boxes[i+1][1]
        arrow = ConnectionPatch((start_pos[0], start_pos[1]-0.5), (end_pos[0], end_pos[1]+0.5),
                               "data", "data", arrowstyle="->", shrinkA=5, shrinkB=5,
                               mutation_scale=20, fc="black")
        ax.add_artist(arrow)

    plt.title('System Architecture Diagram', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('diagrams/system_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_dfd_level0():
    """Create DFD Level 0 (Context Diagram)"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # External entity
    user_rect = FancyBboxPatch((1, 6), 2, 1, boxstyle="round,pad=0.1",
                              facecolor='#FF6B6B', edgecolor='black', linewidth=2)
    ax.add_patch(user_rect)
    ax.text(2, 6.5, 'User', ha='center', va='center', fontsize=12, fontweight='bold')

    # Main process
    main_rect = FancyBboxPatch((4, 3), 2, 2, boxstyle="round,pad=0.1",
                              facecolor='#4ECDC4', edgecolor='black', linewidth=2)
    ax.add_patch(main_rect)
    ax.text(5, 4, 'ShopSense System\n(AI Recommendation)', ha='center', va='center',
            fontsize=10, fontweight='bold')

    # Data store
    data_rect = FancyBboxPatch((7, 1), 2, 1, boxstyle="round,pad=0.1",
                              facecolor='#FFEAA7', edgecolor='black', linewidth=2)
    ax.add_patch(data_rect)
    ax.text(8, 1.5, 'Recommendations', ha='center', va='center', fontsize=10, fontweight='bold')

    # Arrows
    arrow1 = ConnectionPatch((3, 6.5), (4, 4), "data", "data", arrowstyle="->",
                           shrinkA=5, shrinkB=5, mutation_scale=15, fc="black")
    ax.add_artist(arrow1)

    arrow2 = ConnectionPatch((6, 4), (7, 1.5), "data", "data", arrowstyle="->",
                           shrinkA=5, shrinkB=5, mutation_scale=15, fc="black")
    ax.add_artist(arrow2)

    plt.title('DFD Level 0 - Context Diagram', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('diagrams/dfd_level0.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_use_case_diagram():
    """Create Use Case Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Actor (stick figure)
    ax.add_patch(plt.Circle((2, 6), 0.3, fill=False, color='black'))
    ax.plot([2, 2], [5.7, 4.5], color='black', linewidth=2)  # body
    ax.plot([1.7, 2.3], [5.2, 5.5], color='black', linewidth=2)  # arms
    ax.plot([1.8, 2.2], [4.5, 4.2], color='black', linewidth=2)  # legs
    ax.text(2, 7, 'User', ha='center', va='center', fontsize=12, fontweight='bold')

    # System boundary
    system_rect = FancyBboxPatch((5, 2), 5, 4, boxstyle="round,pad=0.1",
                                facecolor='lightblue', edgecolor='black', linewidth=2)
    ax.add_patch(system_rect)
    ax.text(7.5, 5.8, 'ShopSense System', ha='center', va='center', fontsize=12, fontweight='bold')

    # Use cases
    use_cases = [
        ('View Products', 6, 4.5),
        ('Get Recommendations', 7.5, 4.5),
        ('View Insights', 9, 4.5)
    ]

    for text, x, y in use_cases:
        ellipse = patches.Ellipse((x, y), 1.8, 0.8, facecolor='lightyellow', edgecolor='black', linewidth=2)
        ax.add_patch(ellipse)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold')

    # Association lines
    for x, y in [(6, 4.5), (7.5, 4.5), (9, 4.5)]:
        ax.plot([3.3, x-0.9], [6, y], color='black', linewidth=1)

    plt.title('Use Case Diagram', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('diagrams/use_case_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_erd_diagram():
    """Create Entity Relationship Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Entity boxes
    entities = [
        ('Users', 1, 5, ['user_id', 'name', 'age', 'gender']),
        ('Interactions', 6, 5, ['interaction_id', 'user_id', 'product_id', 'rating', 'timestamp']),
        ('Products', 11, 5, ['product_id', 'description', 'category', 'price'])
    ]

    for name, x, y, attrs in entities:
        # Entity header
        header_rect = FancyBboxPatch((x-1.5, y+1), 3, 0.5, boxstyle="round,pad=0.1",
                                   facecolor='#4ECDC4', edgecolor='black', linewidth=2)
        ax.add_patch(header_rect)
        ax.text(x, y+1.25, name, ha='center', va='center', fontsize=12, fontweight='bold')

        # Attributes
        attr_rect = FancyBboxPatch((x-1.5, y-1), 3, 2, boxstyle="round,pad=0.1",
                                  facecolor='white', edgecolor='black', linewidth=2)
        ax.add_patch(attr_rect)

        for i, attr in enumerate(attrs):
            ax.text(x, y+0.5 - i*0.3, attr, ha='center', va='center', fontsize=9)

    # Relationships
    ax.text(4, 5.5, '1', fontsize=14, fontweight='bold')
    ax.text(4, 4.5, 'M', fontsize=14, fontweight='bold')
    ax.text(9, 5.5, 'M', fontsize=14, fontweight='bold')
    ax.text(9, 4.5, '1', fontsize=14, fontweight='bold')

    # Diamonds for relationships
    diamond1 = patches.Polygon([[3.8, 5.2], [4.2, 5.5], [4.6, 5.2], [4.2, 4.9]],
                              facecolor='lightcoral', edgecolor='black', linewidth=2)
    ax.add_patch(diamond1)

    diamond2 = patches.Polygon([[8.8, 5.2], [9.2, 5.5], [9.6, 5.2], [9.2, 4.9]],
                              facecolor='lightcoral', edgecolor='black', linewidth=2)
    ax.add_patch(diamond2)

    plt.title('Entity Relationship Diagram (ERD)', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('diagrams/erd.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_ml_pipeline_diagram():
    """Create ML Pipeline Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Pipeline steps
    steps = [
        ('Raw Data', 5, 11, '#FF6B6B'),
        ('Data Cleaning\nMissing values\nNormalization', 5, 9, '#4ECDC4'),
        ('User-Item Matrix\nCreation', 5, 7, '#45B7D1'),
        ('ALS Training\nProcess\nHyperparameters tuning', 5, 5, '#96CEB4'),
        ('Model Export\n(.pkl file)', 5, 3, '#FFEAA7'),
        ('FastAPI Inference\nLayer', 5, 1.5, '#FDCB6E'),
        ('Streamlit UI\nDisplay', 5, 0, '#6C5CE7')
    ]

    for text, x, y, color in steps:
        rect = FancyBboxPatch((x-2, y-0.5), 4, 1, boxstyle="round,pad=0.1",
                             facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')

    # Arrows
    for i in range(len(steps)-1):
        start_y = steps[i][2] - 0.5
        end_y = steps[i+1][2] + 0.5
        arrow = ConnectionPatch((5, start_y), (5, end_y), "data", "data",
                               arrowstyle="->", shrinkA=5, shrinkB=5,
                               mutation_scale=15, fc="black")
        ax.add_artist(arrow)

    plt.title('Machine Learning Pipeline Diagram', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('diagrams/ml_pipeline.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_deployment_architecture():
    """Create Deployment Architecture Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Components
    components = [
        ('User Browser', 1, 6, '#FF6B6B'),
        ('Streamlit Frontend', 5, 6, '#4ECDC4'),
        ('FastAPI Backend\n(Server)', 5, 4, '#45B7D1'),
        ('ML Model\n(.pkl, ALS)', 5, 2, '#96CEB4'),
        ('Local/Cloud\nStorage', 5, 0, '#FFEAA7')
    ]

    for text, x, y, color in components:
        rect = FancyBboxPatch((x-1.5, y-0.4), 3, 0.8, boxstyle="round,pad=0.1",
                             facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold')

    # Arrows
    arrows = [
        ((2.5, 6), (3.5, 6)),  # User to Streamlit
        ((5, 5.6), (5, 4.4)),  # Streamlit to FastAPI
        ((5, 3.6), (5, 2.4)),  # FastAPI to ML Model
        ((5, 1.6), (5, 0.4))   # ML Model to Storage
    ]

    for start, end in arrows:
        arrow = ConnectionPatch(start, end, "data", "data", arrowstyle="->",
                               shrinkA=5, shrinkB=5, mutation_scale=15, fc="black")
        ax.add_artist(arrow)

    plt.title('Deployment Architecture Diagram', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('diagrams/deployment_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_dfd_level1():
    """Create DFD Level 1"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # External entity
    user_rect = FancyBboxPatch((1, 8), 2, 1, boxstyle="round,pad=0.1",
                              facecolor='#FF6B6B', edgecolor='black', linewidth=2)
    ax.add_patch(user_rect)
    ax.text(2, 8.5, 'User', ha='center', va='center', fontsize=12, fontweight='bold')

    # Processes
    streamlit_rect = FancyBboxPatch((4, 6), 3, 1.5, boxstyle="round,pad=0.1",
                                   facecolor='#4ECDC4', edgecolor='black', linewidth=2)
    ax.add_patch(streamlit_rect)
    ax.text(5.5, 6.75, 'Streamlit\nFrontend', ha='center', va='center', fontsize=10, fontweight='bold')

    fastapi_rect = FancyBboxPatch((4, 3), 3, 1.5, boxstyle="round,pad=0.1",
                                 facecolor='#45B7D1', edgecolor='black', linewidth=2)
    ax.add_patch(fastapi_rect)
    ax.text(5.5, 3.75, 'FastAPI Backend\n/recommend API', ha='center', va='center', fontsize=9, fontweight='bold')

    # Data store
    data_rect = FancyBboxPatch((10, 1), 3, 1, boxstyle="round,pad=0.1",
                              facecolor='#FFEAA7', edgecolor='black', linewidth=2)
    ax.add_patch(data_rect)
    ax.text(11.5, 1.5, 'Data Storage\n(Products, Ratings)', ha='center', va='center', fontsize=9, fontweight='bold')

    # ML Model
    ml_rect = FancyBboxPatch((8, 3), 2, 1, boxstyle="round,pad=0.1",
                            facecolor='#96CEB4', edgecolor='black', linewidth=2)
    ax.add_patch(ml_rect)
    ax.text(9, 3.5, 'ML Model\n(ALS)', ha='center', va='center', fontsize=9, fontweight='bold')

    # Arrows
    arrow1 = ConnectionPatch((3, 8.5), (4, 6.75), "data", "data", arrowstyle="->",
                           shrinkA=5, shrinkB=5, mutation_scale=15, fc="black")
    ax.add_artist(arrow1)

    arrow2 = ConnectionPatch((7, 6.75), (4, 3.75), "data", "data", arrowstyle="->",
                           shrinkA=5, shrinkB=5, mutation_scale=15, fc="black")
    ax.add_artist(arrow2)

    arrow3 = ConnectionPatch((5.5, 4.25), (8, 3.5), "data", "data", arrowstyle="->",
                           shrinkA=5, shrinkB=5, mutation_scale=15, fc="black")
    ax.add_artist(arrow3)

    arrow4 = ConnectionPatch((10, 3.5), (5.5, 4.25), "data", "data", arrowstyle="<->",
                           shrinkA=5, shrinkB=5, mutation_scale=15, fc="black")
    ax.add_artist(arrow4)

    arrow5 = ConnectionPatch((7, 3.75), (10, 1.5), "data", "data", arrowstyle="->",
                           shrinkA=5, shrinkB=5, mutation_scale=15, fc="black")
    ax.add_artist(arrow5)

    # Labels
    ax.text(2.5, 7.5, 'Input: user_id,\nfilters, product search', ha='center', va='center', fontsize=8)
    ax.text(6.5, 5, 'Loads Model', ha='center', va='center', fontsize=8)
    ax.text(6.5, 2.5, 'Output Scores', ha='center', va='center', fontsize=8)

    plt.title('DFD Level 1', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('diagrams/dfd_level1.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_component_architecture():
    """Create Component Architecture Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Main system box
    main_rect = FancyBboxPatch((2, 1), 10, 8, boxstyle="round,pad=0.1",
                              facecolor='lightgray', edgecolor='black', linewidth=3)
    ax.add_patch(main_rect)
    ax.text(7, 8.5, 'ShopSense System', ha='center', va='center', fontsize=16, fontweight='bold')

    # Frontend module
    frontend_rect = FancyBboxPatch((3, 5), 3, 3, boxstyle="round,pad=0.1",
                                  facecolor='#4ECDC4', edgecolor='black', linewidth=2)
    ax.add_patch(frontend_rect)
    ax.text(4.5, 7.5, 'Frontend Module\n(Streamlit)', ha='center', va='center', fontsize=10, fontweight='bold')

    # Backend module
    backend_rect = FancyBboxPatch((7, 5), 3, 3, boxstyle="round,pad=0.1",
                                 facecolor='#45B7D1', edgecolor='black', linewidth=2)
    ax.add_patch(backend_rect)
    ax.text(8.5, 7.5, 'Backend Module\n(FastAPI)', ha='center', va='center', fontsize=10, fontweight='bold')

    # ML Model module
    ml_rect = FancyBboxPatch((5, 2), 4, 2, boxstyle="round,pad=0.1",
                            facecolor='#96CEB4', edgecolor='black', linewidth=2)
    ax.add_patch(ml_rect)
    ax.text(7, 3, 'ML Model Module\nALS Collaborative Filtering\nSimilarity Engine', ha='center', va='center', fontsize=9, fontweight='bold')

    # Data layer
    data_rect = FancyBboxPatch((3, 0.5), 8, 1, boxstyle="round,pad=0.1",
                              facecolor='#FFEAA7', edgecolor='black', linewidth=2)
    ax.add_patch(data_rect)
    ax.text(7, 1, 'Data Layer\nProcessed CSV Files', ha='center', va='center', fontsize=10, fontweight='bold')

    # Component details
    ax.text(4.5, 6.2, 'UI Components\nCharts\nProduct Cards\nFilters', ha='center', va='center', fontsize=8)
    ax.text(8.5, 6.2, 'API Endpoints\nAuth (optional)\nRecommendation\nModel Loading', ha='center', va='center', fontsize=8)

    plt.title('Component Architecture Diagram', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('diagrams/component_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    # Create diagrams directory if it doesn't exist
    os.makedirs('diagrams', exist_ok=True)

    # Generate all diagrams
    print("Generating System Architecture Diagram...")
    create_system_architecture_diagram()

    print("Generating DFD Level 0...")
    create_dfd_level0()

    print("Generating Use Case Diagram...")
    create_use_case_diagram()

    print("Generating ERD...")
    create_erd_diagram()

    print("Generating ML Pipeline...")
    create_ml_pipeline_diagram()

    print("Generating Deployment Architecture...")
    create_deployment_architecture()

    print("Generating DFD Level 1...")
    create_dfd_level1()

    print("Generating Component Architecture...")
    create_component_architecture()

    print("All diagrams generated successfully!")
    print("Check the 'diagrams/' folder for PNG image files.")
