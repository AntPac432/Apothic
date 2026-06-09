#pragma once

#include "CoreMinimal.h"
#include "FResonanceSignature.generated.h"

/**
 * FResonanceSignature
 * 
 * This struct is a core component of the procedural magic system in the Apothic project.
 * It defines the resonance signature of magical entities, which includes properties such as
 * Density, Energy, Temperature, and Gravity. These properties are used to calculate the
 * interactions and effects of magic within the game world.
 * 
 * The values of these properties are clamped between 0.0 and 1000.0 to ensure stability
 * and prevent unrealistic behavior in the simulation.
 */

USTRUCT(BlueprintType)
struct FResonanceSignature
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Resonance")
    float Density;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Resonance")
    float Energy;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Resonance")
    float Temperature;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Resonance")
    float Gravity;

    /**
     * Clamps the values of the properties to ensure they remain within the valid range.
     */
    void ClampValues()
    {
        Density = FMath::Clamp(Density, 0.0f, 1000.0f);
        Energy = FMath::Clamp(Energy, 0.0f, 1000.0f);
        Temperature = FMath::Clamp(Temperature, 0.0f, 1000.0f);
        Gravity = FMath::Clamp(Gravity, 0.0f, 1000.0f);
    }
};