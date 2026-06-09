#include "ApothicGameMode.h"
#include "BaseCharacter.h" // We are telling it where your character code is

AApothicGameMode::AApothicGameMode()
{
    // Force the game to use your custom C++ character, completely bypassing the editor UI settings
    DefaultPawnClass = ABaseCharacter::StaticClass();
}