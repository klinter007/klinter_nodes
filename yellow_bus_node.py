class YellowBus:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL", {"forceInput": False,}),
                "vae": ("VAE", {"forceInput": False,}),
                "pos_prompt": ("CONDITIONING", {"forceInput": False,}),
                "neg_prompt": ("CONDITIONING",  {"forceInput": False,}),
                "latent": ("LATENT", {"forceInput": False,}),
            }
        }

    RETURN_TYPES = ("MODEL", "VAE", "CONDITIONING", "CONDITIONING", "LATENT")
    RETURN_NAMES = ("model", "vae", "pos_prompt", "neg_prompt", "latent")
    FUNCTION = "transfer"

    def transfer(self, model, vae, pos_prompt, neg_prompt, latent):
        return (model, vae, pos_prompt, neg_prompt, latent)
