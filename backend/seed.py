# """
# Seed script for Annapurna Bhakti Bhandar.

# Run with:  python seed.py

# This populates the three main categories (Girls Collection, Certified
# Rudraksha, Rashi Ratna Bracelets) with realistic demo products, and
# creates the initial admin user from ADMIN_EMAIL / ADMIN_PASSWORD in .env.

# These are DEMO products/prices and should be replaced with real shop
# inventory before production use.
# """
# from app.db.database import SessionLocal, engine
# from app.db.base import Base
# from app.models.category import Category
# from app.models.product import Product
# from app.models.admin_user import AdminUser
# from app.core.security import hash_password
# from app.core.config import settings

# Base.metadata.create_all(bind=engine)

# IMG = "https://images.unsplash.com/{}?auto=format&fit=crop&w=800&q=80"

# # Reasonably reliable Unsplash photo ids per theme. Frontend has an
# # onerror fallback to a local placeholder if any of these ever fail.
# GIRLS_IMG = IMG.format("photo-1611652022419-a9419f74343d")
# EARRING_IMG = IMG.format("photo-1630019852942-f89202989a59")
# BANGLE_IMG = IMG.format("photo-1611591437281-460bfbe1220a")
# NECKLACE_IMG = IMG.format("photo-1599643478518-a784e5dc4c8f")
# HAIRCLIP_IMG = IMG.format("photo-1596704017254-9b121068fb31")
# RING_IMG = IMG.format("photo-1603561591411-07134e71a2a9")
# RUDRAKSHA_IMG = IMG.format("photo-1610375461246-83df859d849d")
# MALA_IMG = IMG.format("photo-1611930022073-b7a4ba5fcccd")
# BRACELET_GEM_IMG = IMG.format("photo-1611591437281-460bfbe1220a")

# CATEGORY_IMAGES = {
#     "girls-collection": GIRLS_IMG,
#     "certified-rudraksha": RUDRAKSHA_IMG,
#     "rashi-ratna-bracelets": BRACELET_GEM_IMG,
# }


# def get_or_create_category(db, name, slug, description, image_url):
#     cat = db.query(Category).filter(Category.slug == slug).first()
#     if cat:
#         return cat
#     cat = Category(name=name, slug=slug, description=description, image_url=image_url, is_active=True)
#     db.add(cat)
#     db.commit()
#     db.refresh(cat)
#     return cat


# def upsert_product(db, **kwargs):
#     existing = db.query(Product).filter(Product.slug == kwargs["slug"]).first()
#     if existing:
#         for k, v in kwargs.items():
#             setattr(existing, k, v)
#         db.commit()
#         return existing
#     product = Product(**kwargs)
#     db.add(product)
#     db.commit()
#     return product


# def run():
#     db = SessionLocal()
#     try:
#         # --- Admin user ---
#         admin = db.query(AdminUser).filter(AdminUser.email == settings.ADMIN_EMAIL).first()
#         if not admin:
#             admin = AdminUser(
#                 email=settings.ADMIN_EMAIL,
#                 full_name="Shop Admin",
#                 hashed_password=hash_password(settings.ADMIN_PASSWORD),
#             )
#             db.add(admin)
#             db.commit()
#             print(f"Created admin user: {settings.ADMIN_EMAIL}")
#         else:
#             print(f"Admin user already exists: {settings.ADMIN_EMAIL}")

#         # --- Categories ---
#         girls = get_or_create_category(
#             db, "Girls Collection", "girls-collection",
#             "Beautiful women's fashion accessories — earrings, bangles, necklaces and more.",
#             CATEGORY_IMAGES["girls-collection"],
#         )
#         rudraksha = get_or_create_category(
#             db, "Certified Rudraksha", "certified-rudraksha",
#             "Certified Rudraksha beads, malas and bracelets, traditionally worn for spiritual wellbeing.",
#             CATEGORY_IMAGES["certified-rudraksha"],
#         )
#         rashi = get_or_create_category(
#             db, "Rashi Ratna Bracelets", "rashi-ratna-bracelets",
#             "Gemstone bracelets for all 12 Rashis, traditionally associated with astrological benefits.",
#             CATEGORY_IMAGES["rashi-ratna-bracelets"],
#         )

#         # --- Girls Collection products ---
#         girls_products = [
#             dict(name="Golden Peacock Jhumka Earrings", slug="golden-peacock-jhumka-earrings",
#                  description="Traditional gold-toned peacock design jhumka earrings with pearl drops, perfect for festive occasions.",
#                  price=549, discount_price=449, stock_quantity=25, image_url=EARRING_IMG,
#                  material="Brass, Gold Plated", color="Gold"),
#             dict(name="Kundan Studded Chandbali Earrings", slug="kundan-chandbali-earrings",
#                  description="Elegant Kundan chandbali earrings with intricate stone work, ideal for weddings and parties.",
#                  price=699, discount_price=599, stock_quantity=18, image_url=EARRING_IMG,
#                  material="Alloy, Kundan Stones", color="Gold/White"),
#             dict(name="Rose Gold Layered Bangle Set (Set of 4)", slug="rose-gold-bangle-set",
#                  description="Set of 4 elegant rose gold finish bangles with delicate floral engraving.",
#                  price=799, discount_price=649, stock_quantity=15, image_url=BANGLE_IMG,
#                  material="Metal Alloy", color="Rose Gold", size="2.6 inch"),
#             dict(name="Meenakari Bridal Bangles (Set of 6)", slug="meenakari-bridal-bangles",
#                  description="Colourful Meenakari work bangles, traditional Rajasthani craftsmanship for bridal wear.",
#                  price=899, discount_price=749, stock_quantity=12, image_url=BANGLE_IMG,
#                  material="Metal, Meenakari Enamel", color="Multicolor", size="2.8 inch"),
#             dict(name="Charm Bead Bracelet", slug="charm-bead-bracelet",
#                  description="Trendy stackable charm bead bracelet, adjustable for daily wear.",
#                  price=349, discount_price=299, stock_quantity=30, image_url=BRACELET_GEM_IMG,
#                  material="Beads, Alloy", color="Multicolor"),
#             dict(name="Pearl Drop Layered Necklace", slug="pearl-drop-layered-necklace",
#                  description="Multi-layer necklace with pearl drops and gold-toned chain, pairs beautifully with ethnic wear.",
#                  price=899, discount_price=749, stock_quantity=14, image_url=NECKLACE_IMG,
#                  material="Alloy, Faux Pearl", color="Gold/White"),
#             dict(name="Temple Coin Choker Necklace", slug="temple-coin-choker-necklace",
#                  description="South Indian temple-style coin choker necklace with antique gold finish.",
#                  price=999, discount_price=849, stock_quantity=10, image_url=NECKLACE_IMG,
#                  material="Brass, Antique Finish", color="Antique Gold"),
#             dict(name="Pastel Flower Hair Clips (Set of 3)", slug="pastel-flower-hair-clips",
#                  description="Cute pastel fabric flower hair clips, set of 3, great for daily and festive styling.",
#                  price=249, discount_price=199, stock_quantity=40, image_url=HAIRCLIP_IMG,
#                  material="Fabric, Metal Clip", color="Pastel Mix"),
#             dict(name="Velvet Scrunchie Combo (Pack of 5)", slug="velvet-scrunchie-combo",
#                  description="Soft velvet scrunchies in assorted colours, gentle on hair, pack of 5.",
#                  price=299, discount_price=249, stock_quantity=35, image_url=HAIRCLIP_IMG,
#                  material="Velvet Fabric", color="Assorted"),
#             dict(name="Oxidised Silver Jhumka Earrings", slug="oxidised-silver-jhumka",
#                  description="Boho oxidised silver-finish jhumkas, lightweight and comfortable for daily wear.",
#                  price=449, discount_price=379, stock_quantity=22, image_url=EARRING_IMG,
#                  material="Oxidised Metal", color="Silver"),
#             dict(name="Adjustable Kundan Ring", slug="adjustable-kundan-ring",
#                  description="Adjustable finger ring with Kundan stone centerpiece, one size fits most.",
#                  price=299, discount_price=249, stock_quantity=28, image_url=RING_IMG,
#                  material="Alloy, Kundan", color="Gold/White", size="Adjustable"),
#             dict(name="Designer Maang Tikka", slug="designer-maang-tikka",
#                  description="Traditional maang tikka with dangling pearl, adjustable chain for a perfect fit.",
#                  price=399, discount_price=329, stock_quantity=20, image_url=EARRING_IMG,
#                  material="Alloy, Faux Pearl", color="Gold"),
#         ]
#         for p in girls_products:
#             upsert_product(db, category_id=girls.id, is_active=True, product_type="girls", **p)

#         # --- Rudraksha products ---
#         mukhi_benefits = {
#             "1": "Traditionally associated with focus and spiritual clarity.",
#             "2": "Traditionally associated with harmony in relationships.",
#             "3": "Traditionally associated with confidence and positivity.",
#             "4": "Traditionally associated with creativity and learning.",
#             "5": "Traditionally associated with general wellbeing and balance; the most commonly worn Mukhi.",
#             "6": "Traditionally associated with willpower and determination.",
#             "7": "Traditionally associated with prosperity and stability.",
#             "8": "Traditionally associated with removing obstacles.",
#             "9": "Traditionally associated with courage and energy.",
#             "10": "Traditionally associated with protection and grounding.",
#             "11": "Traditionally associated with self-confidence and focus.",
#             "12": "Traditionally associated with leadership qualities.",
#         }
#         rudraksha_products = []
#         base_price = 399
#         for i in range(1, 13):
#             key = str(i)
#             rudraksha_products.append(dict(
#                 name=f"{i} Mukhi Rudraksha Bead",
#                 slug=f"{i}-mukhi-rudraksha-bead",
#                 description=f"Authentic {i} Mukhi Rudraksha bead, lab-certified for authenticity. "
#                              f"{mukhi_benefits[key]} Comes with a certificate of authenticity.",
#                 price=base_price + (i * 120),
#                 discount_price=base_price + (i * 120) - 50,
#                 stock_quantity=15 + i,
#                 image_url=RUDRAKSHA_IMG,
#                 mukhi=f"{i} Mukhi",
#                 certification="Certified Rudraksha — certificate details available with product",
#                 material="Natural Rudraksha Seed",
#                 size="Standard (varies naturally)",
#             ))
#         rudraksha_products += [
#             dict(name="5 Mukhi Rudraksha Mala (108 Beads)", slug="5-mukhi-rudraksha-mala-108",
#                  description="Traditional 108-bead 5 Mukhi Rudraksha mala for japa and daily wear, certified authentic.",
#                  price=1499, discount_price=1299, stock_quantity=20, image_url=MALA_IMG,
#                  mukhi="5 Mukhi", certification="Certified Rudraksha — certificate details available with product",
#                  material="Natural Rudraksha Seed", size="108 Beads"),
#             dict(name="Rudraksha Bracelet (5 Mukhi, Silver Cap)", slug="rudraksha-bracelet-silver-cap",
#                  description="Elegant Rudraksha bracelet with silver-capped beads, adjustable thread for daily wear.",
#                  price=899, discount_price=749, stock_quantity=25, image_url=MALA_IMG,
#                  mukhi="5 Mukhi", certification="Certified Rudraksha — certificate details available with product",
#                  material="Natural Rudraksha Seed, Silver Cap", size="Adjustable"),
#             dict(name="Rudraksha Combo (Bracelet + Mala)", slug="rudraksha-combo-bracelet-mala",
#                  description="Value combo pack with a 5 Mukhi Rudraksha bracelet and a 27-bead wrist mala, both certified.",
#                  price=1799, discount_price=1499, stock_quantity=12, image_url=MALA_IMG,
#                  mukhi="5 Mukhi", certification="Certified Rudraksha — certificate details available with product",
#                  material="Natural Rudraksha Seed", size="Combo Set"),
#         ]
#         for p in rudraksha_products:
#             upsert_product(db, category_id=rudraksha.id, is_active=True, product_type="rudraksha", **p)

#         # --- Rashi Ratna Bracelet products ---
#         rashi_data = [
#             ("Mesh", "Aries", "Red Coral (Moonga)"),
#             ("Vrishabh", "Taurus", "Diamond / White Sapphire"),
#             ("Mithun", "Gemini", "Emerald (Panna)"),
#             ("Kark", "Cancer", "Pearl (Moti)"),
#             ("Singh", "Leo", "Ruby (Manik)"),
#             ("Kanya", "Virgo", "Emerald (Panna)"),
#             ("Tula", "Libra", "Diamond / White Sapphire"),
#             ("Vrishchik", "Scorpio", "Red Coral (Moonga)"),
#             ("Dhanu", "Sagittarius", "Yellow Sapphire (Pukhraj)"),
#             ("Makar", "Capricorn", "Blue Sapphire (Neelam)"),
#             ("Kumbh", "Aquarius", "Blue Sapphire (Neelam)"),
#             ("Meen", "Pisces", "Yellow Sapphire (Pukhraj)"),
#         ]
#         rashi_products = []
#         for rashi_name, western, gem in rashi_data:
#             rashi_products.append(dict(
#                 name=f"{rashi_name} Rashi {gem.split(' (')[0]} Bracelet",
#                 slug=f"{rashi_name.lower()}-rashi-bracelet",
#                 description=f"Beaded bracelet featuring {gem}, traditionally associated with the {rashi_name} "
#                              f"({western}) Rashi in Vedic astrology. Handcrafted with adjustable thread.",
#                 price=649,
#                 discount_price=549,
#                 stock_quantity=20,
#                 image_url=BRACELET_GEM_IMG,
#                 rashi=rashi_name,
#                 gemstone=gem,
#                 material="Natural Gemstone Beads",
#                 size="Adjustable (Free Size)",
#             ))
#         for p in rashi_products:
#             upsert_product(db, category_id=rashi.id, is_active=True, product_type="rashi", **p)

#         print("Seed data inserted successfully.")
#         print(f"Girls Collection: {len(girls_products)} products")
#         print(f"Certified Rudraksha: {len(rudraksha_products)} products")
#         print(f"Rashi Ratna Bracelets: {len(rashi_products)} products")
#     finally:
#         db.close()


# if __name__ == "__main__":
#     run()


"""
Seed script for Annapurna Bhakti Bhandar.

Run with:  python seed.py

This populates the three main categories (Girls Collection, Certified
Rudraksha, Rashi Ratna Bracelets) with realistic demo products, and
creates the initial admin user from ADMIN_EMAIL / ADMIN_PASSWORD in .env.

These are DEMO products/prices and should be replaced with real shop
inventory before production use.
"""
from app.db.database import SessionLocal, engine
from app.db.base import Base
from app.models.category import Category
from app.models.product import Product
from app.models.admin_user import AdminUser
from app.core.security import hash_password
from app.core.config import settings

Base.metadata.create_all(bind=engine)

IMG = "https://images.unsplash.com/{}?auto=format&fit=crop&w=800&q=80"

# Reasonably reliable Unsplash photo ids per theme. Frontend has an
# onerror fallback to a local placeholder if any of these ever fail.
GIRLS_IMG = IMG.format("photo-1611652022419-a9419f74343d")
EARRING_IMG = IMG.format("photo-1630019852942-f89202989a59")
BANGLE_IMG = IMG.format("photo-1611591437281-460bfbe1220a")
NECKLACE_IMG = IMG.format("photo-1599643478518-a784e5dc4c8f")
HAIRCLIP_IMG = IMG.format("photo-1596704017254-9b121068fb31")
RING_IMG = IMG.format("photo-1603561591411-07134e71a2a9")

# ---------------------------------------------------------------
# Category CARD images (shown on the homepage's 3 big category
# tiles) — these are the owner-supplied real photos.
# Replace these 2 files any time with your own photography:
#   frontend/static/images/rudraksha.jpg
#   frontend/static/images/rashi-bracelet.jpg
# ---------------------------------------------------------------
RUDRAKSHA_CATEGORY_IMG = "/static/images/rudraksha.jpg"
RASHI_CATEGORY_IMG = "/static/images/rashi-bracelet.jpg"

CATEGORY_IMAGES = {
    "girls-collection": GIRLS_IMG,
    "certified-rudraksha": RUDRAKSHA_CATEGORY_IMG,
    "rashi-ratna-bracelets": RASHI_CATEGORY_IMG,
}

# ---------------------------------------------------------------
# Individual PRODUCT images (Rudraksha beads/mala/bracelet and
# each Rashi bracelet). Verified via web search to be genuine
# rudraksha-bead / gemstone-bracelet photos (not random/unrelated
# stock photos). Swap any of these for your own real product
# photos whenever ready — just drop the file into
# frontend/static/images/ and update the path below.
# ---------------------------------------------------------------
RUDRAKSHA_BEAD_IMG = IMG.format("photo-1650809652935-2e5002ba40bf")       # rudraksha beads close-up
RUDRAKSHA_BEAD_IMG_2 = IMG.format("photo-1650809652995-85581c240f19")     # rudraksha beads, same shoot
RUDRAKSHA_MALA_IMG = IMG.format("photo-1685419368164-eb624c946062")       # rudraksha mala hanging
RUDRAKSHA_MALA_IMG_2 = IMG.format("photo-1685419367862-1dd40253bf2b")     # rudraksha mala hanging
RUDRAKSHA_BRACELET_IMG = IMG.format("photo-1622993361118-b6365d859ab6")   # beaded bracelet close-up
RUDRAKSHA_COMBO_IMG = "/static/images/rudraksha.jpg"                      # owner photo

RASHI_PRODUCT_IMAGES = {
    "Mesh": IMG.format("photo-1573446238824-c28afa0cd312"),      # gold-colored gemstone bracelet
    "Vrishabh": IMG.format("photo-1638768892257-8aec93a524e5"),  # bracelets on table
    "Mithun": IMG.format("photo-1632670549453-7a3dfac254a2"),    # bracelets on wooden table
    "Kark": IMG.format("photo-1639363885736-b6685fcbf1f5"),      # close-up bracelet on table
    "Singh": IMG.format("photo-1629890731335-52295b8be1d9"),     # blue and silver beaded bracelet
    "Kanya": IMG.format("photo-1639706188490-876064810182"),     # close-up beaded bracelet on table
    "Tula": IMG.format("photo-1637808248242-57a6265593ed"),      # bracelets group on shell
    "Vrishchik": IMG.format("photo-1636520326725-ef3fe2bf0557"), # bracelets group on shell
    "Dhanu": "/static/images/rashi-bracelet.jpg",                # owner photo
    "Makar": IMG.format("photo-1573446238824-c28afa0cd312"),
    "Kumbh": IMG.format("photo-1638768892257-8aec93a524e5"),
    "Meen": IMG.format("photo-1632670549453-7a3dfac254a2"),
}


def get_or_create_category(db, name, slug, description, image_url):
    cat = db.query(Category).filter(Category.slug == slug).first()
    if cat:
        return cat
    cat = Category(name=name, slug=slug, description=description, image_url=image_url, is_active=True)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def upsert_product(db, **kwargs):
    existing = db.query(Product).filter(Product.slug == kwargs["slug"]).first()
    if existing:
        for k, v in kwargs.items():
            setattr(existing, k, v)
        db.commit()
        return existing
    product = Product(**kwargs)
    db.add(product)
    db.commit()
    return product


def run():
    db = SessionLocal()
    try:
        # --- Admin user ---
        admin = db.query(AdminUser).filter(AdminUser.email == settings.ADMIN_EMAIL).first()
        if not admin:
            admin = AdminUser(
                email=settings.ADMIN_EMAIL,
                full_name="Shop Admin",
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
            )
            db.add(admin)
            db.commit()
            print(f"Created admin user: {settings.ADMIN_EMAIL}")
        else:
            print(f"Admin user already exists: {settings.ADMIN_EMAIL}")

        # --- Categories ---
        girls = get_or_create_category(
            db, "Girls Collection", "girls-collection",
            "Beautiful women's fashion accessories — earrings, bangles, necklaces and more.",
            CATEGORY_IMAGES["girls-collection"],
        )
        rudraksha = get_or_create_category(
            db, "Certified Rudraksha", "certified-rudraksha",
            "Certified Rudraksha beads, malas and bracelets, traditionally worn for spiritual wellbeing.",
            CATEGORY_IMAGES["certified-rudraksha"],
        )
        rashi = get_or_create_category(
            db, "Rashi Ratna Bracelets", "rashi-ratna-bracelets",
            "Gemstone bracelets for all 12 Rashis, traditionally associated with astrological benefits.",
            CATEGORY_IMAGES["rashi-ratna-bracelets"],
        )

        # --- Girls Collection products ---
        girls_products = [
            dict(name="Golden Peacock Jhumka Earrings", slug="golden-peacock-jhumka-earrings",
                 description="Traditional gold-toned peacock design jhumka earrings with pearl drops, perfect for festive occasions.",
                 price=549, discount_price=449, stock_quantity=25, image_url=EARRING_IMG,
                 material="Brass, Gold Plated", color="Gold"),
            dict(name="Kundan Studded Chandbali Earrings", slug="kundan-chandbali-earrings",
                 description="Elegant Kundan chandbali earrings with intricate stone work, ideal for weddings and parties.",
                 price=699, discount_price=599, stock_quantity=18, image_url=EARRING_IMG,
                 material="Alloy, Kundan Stones", color="Gold/White"),
            dict(name="Rose Gold Layered Bangle Set (Set of 4)", slug="rose-gold-bangle-set",
                 description="Set of 4 elegant rose gold finish bangles with delicate floral engraving.",
                 price=799, discount_price=649, stock_quantity=15, image_url=BANGLE_IMG,
                 material="Metal Alloy", color="Rose Gold", size="2.6 inch"),
            dict(name="Meenakari Bridal Bangles (Set of 6)", slug="meenakari-bridal-bangles",
                 description="Colourful Meenakari work bangles, traditional Rajasthani craftsmanship for bridal wear.",
                 price=899, discount_price=749, stock_quantity=12, image_url=BANGLE_IMG,
                 material="Metal, Meenakari Enamel", color="Multicolor", size="2.8 inch"),
            dict(name="Charm Bead Bracelet", slug="charm-bead-bracelet",
                 description="Trendy stackable charm bead bracelet, adjustable for daily wear.",
                 price=349, discount_price=299, stock_quantity=30, image_url=BANGLE_IMG,
                 material="Beads, Alloy", color="Multicolor"),
            dict(name="Pearl Drop Layered Necklace", slug="pearl-drop-layered-necklace",
                 description="Multi-layer necklace with pearl drops and gold-toned chain, pairs beautifully with ethnic wear.",
                 price=899, discount_price=749, stock_quantity=14, image_url=NECKLACE_IMG,
                 material="Alloy, Faux Pearl", color="Gold/White"),
            dict(name="Temple Coin Choker Necklace", slug="temple-coin-choker-necklace",
                 description="South Indian temple-style coin choker necklace with antique gold finish.",
                 price=999, discount_price=849, stock_quantity=10, image_url=NECKLACE_IMG,
                 material="Brass, Antique Finish", color="Antique Gold"),
            dict(name="Pastel Flower Hair Clips (Set of 3)", slug="pastel-flower-hair-clips",
                 description="Cute pastel fabric flower hair clips, set of 3, great for daily and festive styling.",
                 price=249, discount_price=199, stock_quantity=40, image_url=HAIRCLIP_IMG,
                 material="Fabric, Metal Clip", color="Pastel Mix"),
            dict(name="Velvet Scrunchie Combo (Pack of 5)", slug="velvet-scrunchie-combo",
                 description="Soft velvet scrunchies in assorted colours, gentle on hair, pack of 5.",
                 price=299, discount_price=249, stock_quantity=35, image_url=HAIRCLIP_IMG,
                 material="Velvet Fabric", color="Assorted"),
            dict(name="Oxidised Silver Jhumka Earrings", slug="oxidised-silver-jhumka",
                 description="Boho oxidised silver-finish jhumkas, lightweight and comfortable for daily wear.",
                 price=449, discount_price=379, stock_quantity=22, image_url=EARRING_IMG,
                 material="Oxidised Metal", color="Silver"),
            dict(name="Adjustable Kundan Ring", slug="adjustable-kundan-ring",
                 description="Adjustable finger ring with Kundan stone centerpiece, one size fits most.",
                 price=299, discount_price=249, stock_quantity=28, image_url=RING_IMG,
                 material="Alloy, Kundan", color="Gold/White", size="Adjustable"),
            dict(name="Designer Maang Tikka", slug="designer-maang-tikka",
                 description="Traditional maang tikka with dangling pearl, adjustable chain for a perfect fit.",
                 price=399, discount_price=329, stock_quantity=20, image_url=EARRING_IMG,
                 material="Alloy, Faux Pearl", color="Gold"),
        ]
        for p in girls_products:
            upsert_product(db, category_id=girls.id, is_active=True, product_type="girls", **p)

        # --- Rudraksha products ---
        mukhi_benefits = {
            "1": "Traditionally associated with focus and spiritual clarity.",
            "2": "Traditionally associated with harmony in relationships.",
            "3": "Traditionally associated with confidence and positivity.",
            "4": "Traditionally associated with creativity and learning.",
            "5": "Traditionally associated with general wellbeing and balance; the most commonly worn Mukhi.",
            "6": "Traditionally associated with willpower and determination.",
            "7": "Traditionally associated with prosperity and stability.",
            "8": "Traditionally associated with removing obstacles.",
            "9": "Traditionally associated with courage and energy.",
            "10": "Traditionally associated with protection and grounding.",
            "11": "Traditionally associated with self-confidence and focus.",
            "12": "Traditionally associated with leadership qualities.",
        }
        rudraksha_products = []
        base_price = 399
        for i in range(1, 13):
            key = str(i)
            rudraksha_products.append(dict(
                name=f"{i} Mukhi Rudraksha Bead",
                slug=f"{i}-mukhi-rudraksha-bead",
                description=f"Authentic {i} Mukhi Rudraksha bead, lab-certified for authenticity. "
                             f"{mukhi_benefits[key]} Comes with a certificate of authenticity.",
                price=base_price + (i * 120),
                discount_price=base_price + (i * 120) - 50,
                stock_quantity=15 + i,
                image_url=RUDRAKSHA_BEAD_IMG if i % 2 == 1 else RUDRAKSHA_BEAD_IMG_2,
                mukhi=f"{i} Mukhi",
                certification="Certified Rudraksha — certificate details available with product",
                material="Natural Rudraksha Seed",
                size="Standard (varies naturally)",
            ))
        rudraksha_products += [
            dict(name="5 Mukhi Rudraksha Mala (108 Beads)", slug="5-mukhi-rudraksha-mala-108",
                 description="Traditional 108-bead 5 Mukhi Rudraksha mala for japa and daily wear, certified authentic.",
                 price=1499, discount_price=1299, stock_quantity=20, image_url=RUDRAKSHA_MALA_IMG,
                 mukhi="5 Mukhi", certification="Certified Rudraksha — certificate details available with product",
                 material="Natural Rudraksha Seed", size="108 Beads"),
            dict(name="Rudraksha Bracelet (5 Mukhi, Silver Cap)", slug="rudraksha-bracelet-silver-cap",
                 description="Elegant Rudraksha bracelet with silver-capped beads, adjustable thread for daily wear.",
                 price=899, discount_price=749, stock_quantity=25, image_url=RUDRAKSHA_BRACELET_IMG,
                 mukhi="5 Mukhi", certification="Certified Rudraksha — certificate details available with product",
                 material="Natural Rudraksha Seed, Silver Cap", size="Adjustable"),
            dict(name="Rudraksha Combo (Bracelet + Mala)", slug="rudraksha-combo-bracelet-mala",
                 description="Value combo pack with a 5 Mukhi Rudraksha bracelet and a 27-bead wrist mala, both certified.",
                 price=1799, discount_price=1499, stock_quantity=12, image_url=RUDRAKSHA_MALA_IMG_2,
                 mukhi="5 Mukhi", certification="Certified Rudraksha — certificate details available with product",
                 material="Natural Rudraksha Seed", size="Combo Set"),
        ]
        for p in rudraksha_products:
            upsert_product(db, category_id=rudraksha.id, is_active=True, product_type="rudraksha", **p)

        # --- Rashi Ratna Bracelet products ---
        rashi_data = [
            ("Mesh", "Aries", "Red Coral (Moonga)"),
            ("Vrishabh", "Taurus", "Diamond / White Sapphire"),
            ("Mithun", "Gemini", "Emerald (Panna)"),
            ("Kark", "Cancer", "Pearl (Moti)"),
            ("Singh", "Leo", "Ruby (Manik)"),
            ("Kanya", "Virgo", "Emerald (Panna)"),
            ("Tula", "Libra", "Diamond / White Sapphire"),
            ("Vrishchik", "Scorpio", "Red Coral (Moonga)"),
            ("Dhanu", "Sagittarius", "Yellow Sapphire (Pukhraj)"),
            ("Makar", "Capricorn", "Blue Sapphire (Neelam)"),
            ("Kumbh", "Aquarius", "Blue Sapphire (Neelam)"),
            ("Meen", "Pisces", "Yellow Sapphire (Pukhraj)"),
        ]
        rashi_products = []
        for rashi_name, western, gem in rashi_data:
            rashi_products.append(dict(
                name=f"{rashi_name} Rashi {gem.split(' (')[0]} Bracelet",
                slug=f"{rashi_name.lower()}-rashi-bracelet",
                description=f"Beaded bracelet featuring {gem}, traditionally associated with the {rashi_name} "
                             f"({western}) Rashi in Vedic astrology. Handcrafted with adjustable thread.",
                price=649,
                discount_price=549,
                stock_quantity=20,
                image_url=RASHI_PRODUCT_IMAGES.get(rashi_name, RASHI_CATEGORY_IMG),
                rashi=rashi_name,
                gemstone=gem,
                material="Natural Gemstone Beads",
                size="Adjustable (Free Size)",
            ))
        for p in rashi_products:
            upsert_product(db, category_id=rashi.id, is_active=True, product_type="rashi", **p)

        print("Seed data inserted successfully.")
        print(f"Girls Collection: {len(girls_products)} products")
        print(f"Certified Rudraksha: {len(rudraksha_products)} products")
        print(f"Rashi Ratna Bracelets: {len(rashi_products)} products")
    finally:
        db.close()


if __name__ == "__main__":
    run()