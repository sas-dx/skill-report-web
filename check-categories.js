const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function checkCategories() {
  const categories = await prisma.skillCategory.findMany({
    where: { is_deleted: false },
    select: {
      category_code: true,
      category_name: true,
      parent_category_id: true,
      category_level: true,
      category_type: true
    },
    orderBy: [
      { category_level: 'asc' },
      { category_name: 'asc' }
    ]
  });
  
  console.log('=== All categories in database ===');
  categories.forEach(cat => {
    console.log(`Code: ${cat.category_code}`);
    console.log(`  Name: ${cat.category_name}`);
    console.log(`  Parent: ${cat.parent_category_id || 'none'}`);
    console.log(`  Level: ${cat.category_level}`);
    console.log(`  Type: ${cat.category_type}`);
    console.log('---');
  });
  
  const parentCategories = categories.filter(c => !c.parent_category_id || c.category_level === 1);
  const childCategories = categories.filter(c => c.parent_category_id && c.category_level > 1);
  
  console.log(`\n=== Summary ===`);
  console.log(`Total categories: ${categories.length}`);
  console.log(`Parent categories (level 1): ${parentCategories.length}`);
  console.log(`Child categories (level > 1): ${childCategories.length}`);
  
  console.log(`\n=== Parent-Child Relationships ===`);
  parentCategories.forEach(parent => {
    const children = categories.filter(c => c.parent_category_id === parent.category_code);
    console.log(`${parent.category_name} (${parent.category_code})`);
    if (children.length > 0) {
      children.forEach(child => {
        console.log(`  - ${child.category_name} (${child.category_code})`);
      });
    } else {
      console.log(`  - No children`);
    }
  });
}

checkCategories()
  .then(() => prisma.$disconnect())
  .catch(err => {
    console.error(err);
    prisma.$disconnect();
  });