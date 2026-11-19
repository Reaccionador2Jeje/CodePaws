extends Node3D

const PlayerScript = preload("res://scripts/player.gd")
const PetScript = preload("res://scripts/pet.gd")

var _message_label: Label
var _nearby_pet: CodePawsPet
var _message_timer: float = 0.0
const SAVE_PATH := "user://codepaws_save.json"

func _ready() -> void:
	randomize()
	_build_environment()
	_build_world()
	_spawn_player()
	_spawn_pets()
	_build_hud()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_F5:
			_save_game()
		elif event.keycode == KEY_F9:
			_load_game()
		elif event.keycode == KEY_E and _nearby_pet:
			_show_message(_nearby_pet.feed())

func _process(delta: float) -> void:
	_message_timer = maxf(0.0, _message_timer - delta)
	_nearby_pet = null
	var player := get_tree().get_first_node_in_group("player") as Node3D
	if player:
		var closest := 3.2
		for pet in get_tree().get_nodes_in_group("pets"):
			var distance := player.global_position.distance_to(pet.global_position)
			if distance < closest:
				closest = distance
				_nearby_pet = pet as CodePawsPet
	if Input.is_action_just_pressed("interact") and _nearby_pet:
		_show_message(_nearby_pet.interact())
	elif _message_timer <= 0.0:
		if _nearby_pet:
			_message_label.text = "F · Interactuar con " + _nearby_pet.pet_name
		else:
			_message_label.text = "WASD · Mover   ESPACIO · Saltar   F · Acariciar   E · Alimentar   F5/F9 · Guardar/Cargar   ESC · Mouse"

func _build_environment() -> void:
	var world_environment := WorldEnvironment.new()
	var environment := Environment.new()
	environment.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	var sky_material := ProceduralSkyMaterial.new()
	sky_material.sky_top_color = Color(0.16, 0.36, 0.62)
	sky_material.sky_horizon_color = Color(0.72, 0.84, 0.91)
	sky_material.ground_bottom_color = Color(0.16, 0.22, 0.18)
	sky_material.ground_horizon_color = Color(0.56, 0.67, 0.54)
	sky.sky_material = sky_material
	environment.sky = sky
	environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.ambient_light_color = Color(0.72, 0.79, 0.86)
	environment.ambient_light_energy = 0.8
	environment.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	world_environment.environment = environment
	add_child(world_environment)

	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-48.0, -32.0, 0.0)
	sun.light_energy = 1.25
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 90.0
	add_child(sun)

func _build_world() -> void:
	# Gran valle explorable: 700 x 700 metros.
	_add_box("Valley ground", Vector3(0, -0.6, 0), Vector3(700, 1.2, 700), Color(0.28, 0.53, 0.30), true)

	# Ciudad central con avenidas, calles secundarias y plaza.
	_add_box("Main avenue north south", Vector3(0, 0.025, 0), Vector3(15, 0.08, 300), Color(0.22, 0.23, 0.24), false)
	_add_box("Main avenue east west", Vector3(0, 0.03, 0), Vector3(300, 0.08, 15), Color(0.22, 0.23, 0.24), false)
	for road_z in [-90.0, -45.0, 45.0, 90.0]:
		_add_box("City street", Vector3(0, 0.02, road_z), Vector3(230, 0.06, 7), Color(0.34, 0.35, 0.34), false)
	for road_x in [-90.0, -45.0, 45.0, 90.0]:
		_add_box("City street", Vector3(road_x, 0.02, 0), Vector3(7, 0.06, 230), Color(0.34, 0.35, 0.34), false)

	_add_box("Town square", Vector3(0, 0.08, 0), Vector3(32, 0.16, 32), Color(0.72, 0.67, 0.55), false)
	_add_box("Fountain basin", Vector3(0, 0.32, 0), Vector3(7, 0.45, 7), Color(0.25, 0.63, 0.78), false)
	_add_box("Park green", Vector3(62, 0.02, 62), Vector3(35, 0.08, 35), Color(0.20, 0.48, 0.25), false)

	# La casa del jugador, cerca del punto inicial.
	_build_house(Vector3(-13, 0.0, 18), true)
	_build_house(Vector3(24, 0.0, -24))
	_build_house(Vector3(-25, 0.0, -28))
	_build_house(Vector3(28, 0.0, 28))
	_build_house(Vector3(-68, 0.0, 25))
	_build_house(Vector3(68, 0.0, -25))
	_build_city_buildings()

	# Lago y río al este de la ciudad.
	_add_box("Blue lake", Vector3(190, -0.05, 90), Vector3(82, 0.18, 62), Color(0.16, 0.52, 0.76), false)
	_add_box("River", Vector3(245, -0.02, 0), Vector3(22, 0.12, 260), Color(0.19, 0.55, 0.77), false)

	# Cordillera alrededor del valle, visible desde la ciudad.
	var mountain_positions := [
		Vector3(-270, 0, -260), Vector3(-170, 0, -300), Vector3(-35, 0, -315),
		Vector3(115, 0, -305), Vector3(260, 0, -260), Vector3(315, 0, -110),
		Vector3(320, 0, 100), Vector3(260, 0, 270), Vector3(100, 0, 315),
		Vector3(-80, 0, 315), Vector3(-245, 0, 260), Vector3(-320, 0, 80),
		Vector3(-320, 0, -90)
	]
	for i in range(mountain_positions.size()):
		_build_mountain(mountain_positions[i], randf_range(75.0, 125.0), randf_range(95.0, 155.0))

	# Bosques y praderas más allá de la zona urbana.
	for i in range(240):
		var x := randf_range(-295.0, 295.0)
		var z := randf_range(-295.0, 295.0)
		if Vector2(x, z).length() < 112.0:
			continue
		if x > 145.0 and absf(z) < 145.0:
			continue
		_build_tree(Vector3(x, 0.0, z), randf_range(0.85, 1.65))

func _build_city_buildings() -> void:
	var positions := [
		Vector3(-112, 0, -112), Vector3(-55, 0, -112), Vector3(55, 0, -112), Vector3(112, 0, -112),
		Vector3(-112, 0, -55), Vector3(112, 0, -55), Vector3(-112, 0, 55), Vector3(112, 0, 55),
		Vector3(-112, 0, 112), Vector3(-55, 0, 112), Vector3(55, 0, 112), Vector3(112, 0, 112)
	]
	var colors := [Color(0.83, 0.72, 0.57), Color(0.68, 0.77, 0.82), Color(0.82, 0.66, 0.54), Color(0.75, 0.76, 0.67)]
	for i in range(positions.size()):
		var size := Vector3(randf_range(16.0, 23.0), randf_range(12.0, 25.0), randf_range(16.0, 23.0))
		_add_box("City building", positions[i] + Vector3(0, size.y * 0.5, 0), size, colors[i % colors.size()], true)
		_add_box("Flat roof", positions[i] + Vector3(0, size.y + 0.35, 0), Vector3(size.x + 1.0, 0.7, size.z + 1.0), Color(0.35, 0.39, 0.42), false)

func _build_house(origin: Vector3, player_home: bool = false) -> void:
	var wall_color := Color(0.91, 0.80, 0.65) if player_home else Color(0.88, 0.77, 0.61)
	var roof_color := Color(0.22, 0.43, 0.72) if player_home else Color(0.63, 0.27, 0.22)
	_add_box("House walls", origin + Vector3(0, 2.0, 0), Vector3(9, 4, 8), wall_color, true)
	_add_box("House roof", origin + Vector3(0, 4.5, 0), Vector3(10, 1, 9), roof_color, true)
	_add_box("Front door", origin + Vector3(0, 1.0, -4.06), Vector3(1.5, 2, 0.12), Color(0.34, 0.20, 0.13), false)
	_add_box("Window", origin + Vector3(-2.6, 2.5, -4.08), Vector3(1.5, 1.3, 0.12), Color(0.38, 0.72, 0.83), false)

func _build_mountain(origin: Vector3, radius: float, height: float) -> void:
	var mountain := MeshInstance3D.new()
	var mountain_mesh := CylinderMesh.new()
	mountain_mesh.top_radius = 1.5
	mountain_mesh.bottom_radius = radius
	mountain_mesh.height = height
	mountain_mesh.radial_segments = 9
	mountain_mesh.rings = 4
	mountain.mesh = mountain_mesh
	mountain.position = origin + Vector3(0, height * 0.5 - 1.0, 0)
	mountain.material_override = _material(Color(0.35, 0.39, 0.38))
	add_child(mountain)

	var snow := MeshInstance3D.new()
	var snow_mesh := CylinderMesh.new()
	snow_mesh.top_radius = 0.0
	snow_mesh.bottom_radius = radius * 0.24
	snow_mesh.height = height * 0.28
	snow_mesh.radial_segments = 9
	snow.mesh = snow_mesh
	snow.position = origin + Vector3(0, height * 0.88, 0)
	snow.material_override = _material(Color(0.88, 0.92, 0.94))
	add_child(snow)

func _build_tree(origin: Vector3, scale_factor: float) -> void:
	var trunk := MeshInstance3D.new()
	var trunk_mesh := CylinderMesh.new()
	trunk_mesh.top_radius = 0.22 * scale_factor
	trunk_mesh.bottom_radius = 0.34 * scale_factor
	trunk_mesh.height = 2.0 * scale_factor
	trunk.mesh = trunk_mesh
	trunk.position = origin + Vector3(0, scale_factor, 0)
	trunk.material_override = _material(Color(0.37, 0.23, 0.13))
	add_child(trunk)

	var crown := MeshInstance3D.new()
	var crown_mesh := SphereMesh.new()
	crown_mesh.radius = 1.35 * scale_factor
	crown_mesh.height = 2.7 * scale_factor
	crown.mesh = crown_mesh
	crown.position = origin + Vector3(0, 2.5 * scale_factor, 0)
	crown.material_override = _material(Color(0.16 + randf() * 0.08, 0.42 + randf() * 0.12, 0.22))
	add_child(crown)

func _spawn_player() -> void:
	var player := PlayerScript.new() as CharacterBody3D
	player.position = Vector3(0, 0.1, 8)
	add_child(player)

func _spawn_pets() -> void:
	var definitions := [
		["Py", Color(0.25, 0.68, 0.39), Vector3(-3, 0, 2)],
		["Ferris", Color(0.85, 0.30, 0.22), Vector3(3, 0, 0)],
		["Gopher", Color(0.28, 0.62, 0.82), Vector3(-5, 0, -4)],
		["Duke", Color(0.82, 0.48, 0.23), Vector3(5, 0, -5)]
	]
	for definition in definitions:
		var pet := PetScript.new() as CodePawsPet
		pet.pet_name = definition[0]
		pet.body_color = definition[1]
		pet.position = definition[2]
		add_child(pet)

func _build_hud() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	var title := Label.new()
	title.text = "CODEPAWS 3D  ·  OPEN WORLD"
	title.position = Vector2(24, 18)
	title.add_theme_font_size_override("font_size", 25)
	title.add_theme_color_override("font_color", Color(1.0, 0.96, 0.83))
	layer.add_child(title)

	_message_label = Label.new()
	_message_label.position = Vector2(24, 665)
	_message_label.add_theme_font_size_override("font_size", 16)
	_message_label.add_theme_color_override("font_color", Color.WHITE)
	layer.add_child(_message_label)

	var hint := Label.new()
	hint.text = "TU CASA · CIUDAD · LAGO · BOSQUES · CORDILLERA"
	hint.position = Vector2(24, 55)
	hint.add_theme_font_size_override("font_size", 13)
	hint.add_theme_color_override("font_color", Color(0.85, 0.94, 0.89))
	layer.add_child(hint)

func _show_message(message: String) -> void:
	_message_label.text = message
	_message_timer = 3.0

func _add_box(object_name: String, position: Vector3, size: Vector3, color: Color, solid: bool) -> void:
	var body := StaticBody3D.new() if solid else Node3D.new()
	body.name = object_name
	body.position = position
	var mesh_instance := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = size
	mesh_instance.mesh = box
	mesh_instance.material_override = _material(color)
	body.add_child(mesh_instance)
	if solid:
		var collision := CollisionShape3D.new()
		var shape := BoxShape3D.new()
		shape.size = size
		collision.shape = shape
		body.add_child(collision)
	add_child(body)

func _material(color: Color) -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	material.roughness = 0.9
	return material

func _save_game() -> void:
	var player := get_tree().get_first_node_in_group("player") as Node3D
	var pet_data: Array[Dictionary] = []
	for pet in get_tree().get_nodes_in_group("pets"):
		pet_data.append((pet as CodePawsPet).to_save_data())
	var data := {
		"version": 1,
		"player_position": [player.global_position.x, player.global_position.y, player.global_position.z] if player else [0.0, 0.0, 8.0],
		"pets": pet_data
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		_show_message("No se pudo guardar la partida.")
		return
	file.store_string(JSON.stringify(data))
	file.close()
	_show_message("Partida guardada correctamente.")

func _load_game() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		_show_message("Todavía no existe una partida guardada.")
		return
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		_show_message("No se pudo abrir la partida.")
		return
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	file.close()
	if not parsed is Dictionary:
		_show_message("El archivo de guardado no es válido.")
		return
	var player := get_tree().get_first_node_in_group("player") as Node3D
	var player_position: Array = parsed.get("player_position", [])
	if player and player_position.size() == 3:
		player.global_position = Vector3(float(player_position[0]), float(player_position[1]), float(player_position[2]))
	var saved_pets: Array = parsed.get("pets", [])
	var current_pets := get_tree().get_nodes_in_group("pets")
	for index in range(mini(saved_pets.size(), current_pets.size())):
		if saved_pets[index] is Dictionary:
			(current_pets[index] as CodePawsPet).load_save_data(saved_pets[index])
	_show_message("Partida cargada correctamente.")
