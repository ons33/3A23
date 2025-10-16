<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use App\Repository\AuthorRepository;
use Doctrine\Persistence\ManagerRegistry;
use App\Entity\Author;
use App\Form\AuthorType;
use Symfony\Component\HttpFoundation\Request;
use Doctrine\ORM\EntityManagerInterface;

//  #[Route('/author')]
final class AuthorController extends AbstractController
{
    #[Route('/i', name: 'app_author')]
    public function index(): Response
    {
        return $this->render('author/index.html.twig', [
            'controller_name' => 'AuthorController',
        ]);
    }

     #[Route('/getAllAuth', name: 'get_author')]
    public function getAll(AuthorRepository $authRepo  ): Response
    {
        $authors = $authRepo->findAll();


        return $this->render('author/index.html.twig', [
            'authors' => $authors,
        ]);
    }

      #[Route('/addAuth', name: 'add_author')]
    public function addAuth(ManagerRegistry $em ,Request $request): Response
    {
        $auth1= new Author();
       $form=$this->createForm(AuthorType::class,$auth1);
        $form->handleRequest($request);
        if($form->isSubmitted()){
            $em->getManager()->persist($auth1);
            $em->getManager()->flush();
            return $this->redirectToRoute('get_author');
        }
        return $this->render('author/add.html.twig', [
            'f'=>$form->createView()
        ]);
        


        return New Response(' author added');
    }
     #[Route('/deleteAuth/{id}', name: 'app_delete')]
    public function deleteAuthor(ManagerRegistry $em,AuthorRepository $authRepo,$id): Response
    {
          $auth = $authRepo->find($id);
        $em->getManager()->remove($auth);
        $em->getManager()->flush();
        return $this->redirectToRoute('get_author');
    }

        #[Route('/updateAuth/{id}',name:'app_author_update')]
    public function updateAuthor(Request $req,EntityManagerInterface $em,Author $author
    ,AuthorRepository $repo){
        //$author = $repo->find($id);
        $form = $this->createForm(AuthorType::class,$author);
        $form->handleRequest($req);
        if($form->isSubmitted())
        {
        $em->flush();
        return $this->redirectToRoute('get_author');
        }
       // $author->setName("author 1");
        //$author->setEmail("author1@gmail.com");

        return $this->render('author/update.html.twig',[
            'f'=>$form->createView()
        ]);
    }

}
