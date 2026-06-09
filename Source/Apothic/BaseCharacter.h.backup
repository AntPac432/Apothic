#pragma once

#include "CoreMinimal.h"
#include "InputActionValue.h"
#include "GameFramework/Character.h"
#include "BaseCharacter.generated.h"

UCLASS()
class APOTHIC_API ABaseCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    ABaseCharacter();

protected:
    virtual void BeginPlay() override;

public:	
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;
    virtual void Tick(float DeltaTime) override;

private:
    void MoveForward(const FInputActionValue& Value);
    void MoveRight(const FInputActionValue& Value);
    void Turn(const FInputActionValue& Value);
    void LookUp(const FInputActionValue& Value);
    void StartSprint();
    void StopSprint();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Movement", meta = (AllowPrivateAccess = "true"))
    bool bIsSprinting;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Input", meta = (AllowPrivateAccess = "true"))
    class UInputAction* MoveAction;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Input", meta = (AllowPrivateAccess = "true"))
    class UInputAction* LookAction;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Input", meta = (AllowPrivateAccess = "true"))
    class UInputAction* SprintAction;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    class USpringArmComponent* CameraBoom;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    class UCameraComponent* FollowCamera;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Movement", meta = (AllowPrivateAccess = "true"))
    float WalkSpeed = 300.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Movement", meta = (AllowPrivateAccess = "true"))
    float SprintSpeed = 600.0f;
};