#include <SDL.h>

//In order to access SDL_image features, we must include SDL_image.h
#include <SDL_image.h>

#undef main

int main(int argc, char** args)
{
    SDL_Init(SDL_INIT_EVERYTHING);
    //For loading PNG images
 IMG_Init(IMG_INIT_PNG);
    SDL_Event input;
    short int quit = 0;

    SDL_Texture* texture = NULL;
    SDL_Surface* temp = IMG_Load("../face.png");
	if(!temp) {
	    printf("IMG_Load: %s\n", IMG_GetError());
	    // handle error
	    return -1;
	}
	int width = temp->w;
	int height = temp->h;
	printf("%d:%d\n", width, height);
    //Deleting the temporary surface
 	SDL_FreeSurface(temp);

    //Deleting the texture
	 SDL_DestroyTexture(texture);

    //For quitting IMG systems
 	IMG_Quit();

    SDL_Quit();

    return 0;
}