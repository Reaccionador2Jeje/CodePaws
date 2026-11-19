extends CharacterBody3D
class_name CodePawsPlayer

@export var move_speed: float = 7.0
@export var jump_velocity: float = 7.5
@export var mouse_sensitivity: float = 0.0025

var gravity: float = float(ProjectSettings.get_setting("physics/3d/default_gravity"))
var camera_pivot: Node3D
var spring_arm: SpringArm3D

func _ready() -> void:
	name = "Player"
	add_to_group("player")

	var collider := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.38
	capsule.height = 1.8
	collider.shape = capsule
	collider.position.y = 0.9
	add_child(collider)

	var body_mesh := MeshInstance3D.new()
	var body := CapsuleMesh.new()
	body.radius = 0.38
	body.height = 1.8
	body_mesh.mesh = body
	body_mesh.position.y = 0.9
	var material := StandardMaterial3D.new()
	material.albedo_color = Color(0.24, 0.48, 0.78)
	material.roughness = 0.82
	body_mesh.material_override = material
	add_child(body_mesh)

	# La cámara queda independiente del giro visual del personaje.
	camera_pivot = Node3D.new()
	camera_pivot.set_as_top_level(true)
	camera_pivot.global_position = global_position + Vector3(0, 1.45, 0)
	get_tree().root.add_child(camera_pivot)

	spring_arm = SpringArm3D.new()
	spring_arm.spring_length = 6.5
	spring_arm.margin = 0.2
	camera_pivot.add_child(spring_arm)

	var camera := Camera3D.new()
	camera.current = true
	camera.fov = 72.0
	spring_arm.add_child(camera)
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _exit_tree() -> void:
	if is_instance_valid(camera_pivot):
		camera_pivot.queue_free()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		camera_pivot.rotate_y(-event.relative.x * mouse_sensitivity)
		camera_pivot.rotation.x = clampf(
			camera_pivot.rotation.x - event.relative.y * mouse_sensitivity,
			deg_to_rad(-48.0), deg_to_rad(35.0)
		)
	elif event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _physics_process(delta: float) -> void:
	# Seguir al jugador sin heredar su rotación.
	if is_instance_valid(camera_pivot):
		camera_pivot.global_position = global_position + Vector3(0, 1.45, 0)

	if not is_on_floor():
		velocity.y -= gravity * delta
	elif Input.is_action_just_pressed("jump"):
		velocity.y = jump_velocity

	var input_vector := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var forward := -camera_pivot.global_basis.z
	var right := camera_pivot.global_basis.x
	var direction := (right * input_vector.x + forward * -input_vector.y).normalized()

	if direction.length_squared() > 0.001:
		velocity.x = direction.x * move_speed
		velocity.z = direction.z * move_speed
		var target_yaw := atan2(-direction.x, -direction.z)
		rotation.y = lerp_angle(rotation.y, target_yaw, delta * 10.0)
	else:
		velocity.x = move_toward(velocity.x, 0.0, move_speed * 5.0 * delta)
		velocity.z = move_toward(velocity.z, 0.0, move_speed * 5.0 * delta)

	move_and_slide()
