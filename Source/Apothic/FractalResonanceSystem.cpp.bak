#include "FractalResonanceSystem.h"
#include "GameplayTagContainer.h"
#include "AbilitySystemComponent.h"

UFractalResonanceSystem::UFractalResonanceSystem()
{
    // Initialize default values for attributes
    CosmicEnergy = FGameplayAttributeData(100.0f); // Default starting value
    ResonanceLevel = FGameplayAttributeData(1.0f); // Default starting level
}

void UFractalResonanceSystem::GenerateDynamicNodes(const FGameplayTagContainer& ActionTags)
{
    // Example logic for evaluating action-triggered GameplayTags
    if (ActionTags.HasTag(FGameplayTag::RequestGameplayTag(FName("Action.Attack.Melee"))))
    {
        // Logic for melee attack
        CosmicEnergy.SetCurrentValue(CosmicEnergy.GetCurrentValue() - 10.0f);
    }
    if (ActionTags.HasTag(FGameplayTag::RequestGameplayTag(FName("Element.Fire"))))
    {
        // Logic for fire element
        ResonanceLevel.SetCurrentValue(ResonanceLevel.GetCurrentValue() + 0.5f);
    }
    // Additional logic for other tags can be added here
}

void UFractalResonanceSystem::CalculateAttributeScaling()
{
    // Example mathematical scaling formula based on proficiency
    float ProficiencyMultiplier = 1.0f + (ResonanceLevel.GetCurrentValue() * 0.1f);
    CosmicEnergy.SetBaseValue(CosmicEnergy.GetBaseValue() * ProficiencyMultiplier);
    ResonanceLevel.SetBaseValue(ResonanceLevel.GetBaseValue() * ProficiencyMultiplier);
}