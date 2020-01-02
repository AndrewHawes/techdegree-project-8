def mineral_filters(request):
    mineral_groups = [
        'Arsenates', 'Borates', 'Carbonates', 'Halides', 'Native Elements',
        'Organic Minerals', 'Oxides', 'Phosphates', 'Silicates', 'Sulfates',
        'Sulfides', 'Sulfosalts', 'Other'
    ]

    mineral_colors = [
        'Black', 'Blue', 'Bronze', 'Brown', 'Golden', 'Gray', 'Green', 'Orange',
        'Olive', 'Pink', 'Purple', 'Red', 'Silver', 'Violet', 'White', 'Yellow'
    ]

    mineral_lusters = [
        'Adamantine', 'Brilliant', 'Dull', 'Earthy', 'Glassy', 'Greasy',
        'Metallic', 'Pearly', 'Resinous', 'Silky', 'Splendent', 'Subadamantine',
        'Submetallic', 'Subresinous', 'Subvitreous', 'Vitreous', 'Waxy'
    ]
    return {'mineral_groups': mineral_groups,
            'mineral_colors': mineral_colors,
            'mineral_lusters': mineral_lusters}