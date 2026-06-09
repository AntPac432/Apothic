#include "BaseCharacter.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "GameFramework/PlayerController.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "InputMappingContext.h"
#include "InputAction.h"

ABaseCharacter::ABaseCharacter()
{
    bIsSprinting = false;

    // Create a camera boom (pulls in towards the player if there is a collision)
    CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
    CameraBoom->SetupAttachment(RootComponent);
    CameraBoom->TargetArmLength = 300.0f; // The camera follows at this distance behind the character
    CameraBoom->bUsePawnControlRotation = true; // Rotate the arm based on the controller

    // Create a follow camera
    FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
    FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName); // Attach the camera to the end of the boom and let the boom adjust to match the controller orientation
    FollowCamera->bUsePawnControlRotation = false; // Camera does not rotate relative to arm

    // Set default movement speeds
    GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
}

void ABaseCharacter::BeginPlay()
{
    Super::BeginPlay();

    if (APlayerController* PlayerController = Cast<APlayerController>(GetController()))
    {
        if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer()))
        {
            // Add input mapping context here if needed
            UInputMappingContext* PlayerInputMapping = LoadObject<UInputMappingContext>(nullptr, TEXT("/Game/Input/PlayerInputMapping.PlayerInputMapping"));
            if (PlayerInputMapping)
            {
                Subsystem->AddMappingContext(PlayerInputMapping, 0);
            }
        }
    }
}

void ABaseCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    if (UEnhancedInputComponent* EnhancedInputComponent = Cast<UEnhancedInputComponent>(PlayerInputComponent))
    {
        EnhancedInputComponent->BindAction(MoveAction, ETriggerEvent::Triggered, this, &ABaseCharacter::MoveForward);
        EnhancedInputComponent->BindAction(MoveAction, ETriggerEvent::Triggered, this, &ABaseCharacter::MoveRight);
        EnhancedInputComponent->BindAction(LookAction, ETriggerEvent::Triggered, this, &ABaseCharacter::Turn);
        EnhancedInputComponent->BindAction(LookAction, ETriggerEvent::Triggered, this, &ABaseCharacter::LookUp);
        EnhancedInputComponent->BindAction(SprintAction, ETriggerEvent::Started, this, &ABaseCharacter::StartSprint);
        EnhancedInputComponent->BindAction(SprintAction, ETriggerEvent::Completed, this, &ABaseCharacter::StopSprint);
    }
}

void ABaseCharacter::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    // Update movement speed based on sprinting state
    GetCharacterMovement()->MaxWalkSpeed = bIsSprinting ? SprintSpeed : WalkSpeed;
}

void ABaseCharacter::MoveForward(const FInputActionValue& Value)
{
    if (Controller && Value.Get<float>() != 0.0f)
    {
        const FRotator Rotation = Controller->GetControlRotation();
        const FRotator YawRotation(0, Rotation.Yaw, 0);
        const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
        AddMovementInput(Direction, Value.Get<float>());
    }
}

void ABaseCharacter::MoveRight(const FInputActionValue& Value)
{
    if (Controller && Value.Get<float>() != 0.0f)
    {
        const FRotator Rotation = Controller->GetControlRotation();
        const FRotator YawRotation(0, Rotation.Yaw, 0);
        const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y);
        AddMovementInput(Direction, Value.Get<float>());
    }
}

void ABaseCharacter::Turn(const FInputActionValue& Value)
{
    AddControllerYawInput(Value.Get<float>());
}

void ABaseCharacter::LookUp(const FInputActionValue& Value)
{
    AddControllerPitchInput(Value.Get<float>());
}

void ABaseCharacter::StartSprint()
{
    bIsSprinting = true;
}

void ABaseCharacter::StopSprint()
{
    bIsSprinting = false;
}