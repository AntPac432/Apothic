#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "EnhancedInputComponent.h"
#include "InputActionValue.h"
#include "ApothicCharacter.generated.h"

UCLASS()
class AApothicCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    // Constructor
    AApothicCharacter();

protected:
    // Called to bind functionality to input
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

    // Input functions
    void Move(const FInputActionValue& Value);
    void Look(const FInputActionValue& Value);

    // Input properties
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
    class UInputMappingContext* InputMappingContext;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
    class UInputAction* MoveAction;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Input)
    class UInputAction* LookAction;
};