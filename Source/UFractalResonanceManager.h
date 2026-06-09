#pragma once

#include "CoreMinimal.h"
#include "FResonanceSignature.h"
#include "UFractalResonanceManager.generated.h"

UCLASS()
class APOTHIC_API UFractalResonanceManager : public UObject
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "Resonance")
    FResonanceSignature CombineSignatures(const FResonanceSignature& Item, const FResonanceSignature& Biome) const;
};