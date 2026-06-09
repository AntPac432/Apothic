#include "UFractalResonanceManager.h"

FResonanceSignature UFractalResonanceManager::CombineSignatures(const FResonanceSignature& Item, const FResonanceSignature& Biome) const
{
    FResonanceSignature Result;
    Result.Density = Item.Density * Biome.Density;
    Result.Energy = Item.Energy * Biome.Energy;
    Result.Temperature = Item.Temperature * Biome.Temperature;
    Result.Gravity = Item.Gravity * Biome.Gravity;
    return Result;
}