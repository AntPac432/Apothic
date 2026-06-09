#pragma once

#include "CoreMinimal.h"
#include "GameplayTagContainer.h"
#include "AttributeSet.h"
#include "AbilitySystemComponent.h"
#include "FractalResonanceSystem.generated.h"

// Macro to define attribute accessors
#define ATTRIBUTE_ACCESSORS(ClassName, PropertyName) \
    GAMEPLAYATTRIBUTE_PROPERTY_GETTER(ClassName, PropertyName) \
    GAMEPLAYATTRIBUTE_VALUE_GETTER(PropertyName) \
    GAMEPLAYATTRIBUTE_VALUE_SETTER(PropertyName) \
    GAMEPLAYATTRIBUTE_VALUE_INITTER(PropertyName)

UCLASS()
class APOTHIC_API UFractalResonanceSystem : public UAttributeSet
{
    GENERATED_BODY()

public:
    UFractalResonanceSystem();

    // Attributes
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    FGameplayAttributeData CosmicEnergy;
    ATTRIBUTE_ACCESSORS(UFractalResonanceSystem, CosmicEnergy)

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    FGameplayAttributeData ResonanceLevel;
    ATTRIBUTE_ACCESSORS(UFractalResonanceSystem, ResonanceLevel)

    // Function to handle dynamic node generation based on GameplayTags
    UFUNCTION(BlueprintCallable, Category = "Fractal Resonance")
    void GenerateDynamicNodes(const FGameplayTagContainer& ActionTags);

protected:
    // Function to calculate attribute scaling
    UFUNCTION(BlueprintCallable, Category = "Fractal Resonance")
    void CalculateAttributeScaling();
};