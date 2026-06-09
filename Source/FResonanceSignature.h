#pragma once

#include "CoreMinimal.h"
#include "FResonanceSignature.generated.h"

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
};